from collections import deque
from typing import Any

import polars as pl


class PreordedTraverse:
    def __init__(
        self,
        data: pl.DataFrame,
        child: str,
        parent: str,
        level: str,
        left: str,
        right: str,
        max_iter: int = 10000,
    ) -> None:
        self._data = data
        self._child = child
        self._parent = parent
        self._level = level
        self._left = left
        self._right = right
        self._max_iter = max_iter
        self._stack: deque[int] = deque()
        self._rows: list[dict[str, Any]] = [
            dict(row) for row in self._data.iter_rows(named=True)
        ]

    @property
    def data(self) -> pl.DataFrame:
        return self._data

    def fit_transform(self) -> None:
        self.fit()
        self.transform()

    def fit(self) -> None:
        self.fit_validate()
        self.fit_reset()

    def fit_validate(self) -> None:
        if self._data.is_empty():
            msg: str = "The data to traverse is empty."
            raise ValueError(msg)
        if self._stack:
            msg = "The stack must be empty at the start. Weird!"
            raise ValueError(msg)
        if self._max_iter < 10:
            msg = f"{self._max_iter=}, it must be >= 10."
            raise AssertionError(msg)

    def fit_reset(self) -> None:
        self._data = self._data.with_columns(
            pl.lit(0).cast(pl.Int64).alias(self._level),
            pl.lit(0).cast(pl.Int64).alias(self._left),
            pl.lit(0).cast(pl.Int64).alias(self._right),
        )
        self._rows = [dict(row) for row in self._data.iter_rows(named=True)]

    def transform(self) -> None:
        self.set_root()
        self.traverse()
        self.audit()

    def set_root(self) -> None:
        """Set the root."""
        index_df = self._data.with_row_index(name="__idx")
        root_idx = (
            index_df.filter(pl.col(self._child) == pl.col(self._parent))
            .get_column("__idx")
            .to_list()
        )
        nroot = len(root_idx)
        if nroot != 1:
            msg = f"{nroot} roots found. There must be a unique root."
            raise AssertionError(msg)

        root_pos = root_idx[0]
        self._rows[root_pos][self._left] = 1
        self._stack.append(root_pos)
        if len(self._stack) != 1:
            msg = "There must be exactly 1 element, the root, in the stack."
            raise AssertionError(msg)
        self._data = pl.DataFrame(self._rows, schema=self._data.schema)

    def traverse(self) -> None:
        stack = self._stack
        level_no: int = 0
        path_no: int = 1
        while stack:
            path_no += 1
            a_node = self._rows[stack[-1]][self._child]
            child_idx = [
                idx
                for idx, row in enumerate(self._rows)
                if row[self._parent] == a_node and row[self._left] == 0
            ]
            if child_idx:
                level_no += 1
                idx = child_idx[0]
                self._rows[idx][self._level] = level_no
                self._rows[idx][self._left] = path_no
                stack.append(idx)
            else:
                level_no -= 1
                idx = stack.pop()
                self._rows[idx][self._right] = path_no
            if path_no > self._max_iter:
                msg: str = f"""
                POT terminated because {path_no=} greater than {self._max_iter=}.
                Maybe you should increase `max_iter`."""
                raise ValueError(msg)
        nstack = len(stack)
        if nstack:
            msg = f"""
            The stack must be empty at the end. It has {nstack} elements in it.
            This implies that not all rows have been traversed.
            """
            raise AssertionError(msg)
        self._data = pl.DataFrame(self._rows, schema=self._data.schema)
        self._stack = stack

    def audit(self) -> None:
        if not self._rows:
            raise ValueError("The traversal returned empty data. Weird!")
        left_count = sum(1 for row in self._rows if row[self._left] == 1)
        if left_count != 1:
            msg: str = (
                f"There must be 1 left id equal to 1, there is {left_count} of them."
            )
            raise AssertionError(msg)

        root_idx = next(
            idx for idx, row in enumerate(self._rows) if row[self._left] == 1
        )
        if self._rows[root_idx][self._level] != 0:
            raise AssertionError("The level must be 0 at the root.")

        root_right = self._rows[root_idx][self._right]
        target_right = 2 * len(self._rows)
        if root_right != target_right:
            msg = f"The root has right value of {root_right}, it should be {target_right}."
            raise AssertionError(msg)
        self._data = pl.DataFrame(self._rows, schema=self._data.schema)
