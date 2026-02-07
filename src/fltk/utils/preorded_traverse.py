import pandas as pd
from collections import deque

class PreordedTraverse:
    def __init__(self,data: pd.DataFrame,child: str,parent: str,level: str,left: str,right: str, max_iter: int = 10000)->None:
        self._data=data
        self._child=child
        self._parent=parent
        self._level=level
        self._left=left
        self._right=right
        self._max_iter = max_iter
        self._stack: deque = deque()
        
    @property
    def data(self)->pd.DataFrame:
        return self._data
        
    def fit_exec(self)->None:
        self.fit()
        self.exec()
    
    def fit(self)->None:
        self.fit_validate()
        self.fit_reset()
    
    def fit_validate(self)->None:
        if self._data.empty:
            msg: str = "The data to traverse is empty."
            raise ValueError(msg)
        if self._stack:
            msg = "The stack must be empty at the start. Weird!"
            raise ValueError(msg)
        if self._max_iter < 10:
            msg = f"max_iter must be >= 10. It is {self._max_iter=}."
            raise ValueError(msg)
        
    def fit_reset(self)->None:
        self._data[self._level] = 0
        self._data[self._left] = 0
        self._data[self._right] = 0
        
    def exec(self)->None:
        self.set_root()
        self.traverse()
        self.audit()
        
    def set_root(self)->None:
        """Set the root."""
        data = self._data
        sel = data.loc[(data[self._child] == data[self._parent])]
        nroot = sel.shape[0]
        if nroot != 1:
            msg = f"{nroot} roots found. There must be a unique root."
            raise AssertionError(msg)
        data.loc[sel.index, self._left] = 1
        self._stack.append(sel.index)
        if len(self._stack) != 1:
            msg = "There must be exactly 1 element, the root, in the stack."
            raise AssertionError(msg)
        self._data=data
        
    def traverse(self)->None:
        data = self._data
        stack=self._stack
        level_no: int = 0
        path_no: int = 1
        while stack:
            path_no += 1
            a_node = data.loc[stack[-1], self._child]
            sel = (data[self._parent].isin(a_node)) & (data[self._left] == 0)
            if any(sel):
                level_no += 1
                idx = data.loc[sel].head(1).index
                data.loc[idx, [self._level, self._left]] = level_no, path_no
                stack.append(idx)
            else:
                level_no -= 1
                idx = stack.pop()
                data.loc[idx, self._right] = path_no
            if path_no > self._max_iter:
                msg: str = f"""
                POT terminated because {path_no=} greater than {self._max_iter=}.
                Maybe you should increase `max_iter`."""
                raise StopIteration(msg)
        nstack = len(stack)
        if nstack:
            msg = f"""
            The stack must be empty at the end. It has {nstack} elements in it.
            This implies that not all rows have been traversed.
            """
            raise AssertionError(msg)
        self._data=data
        self._stack=stack
        
    def audit(self) -> None:
        if self._data.empty:
            raise ValueError("The traversal returned empty data. Weird!")
        data = self._data
        sel = data[self._left] == 1
        check = sel.sum()
        if check != 1:
            msg: str = f"There must be 1 left id equal to 1, there is {check} of them."
            raise AssertionError(msg)
        
        check = (data.loc[sel, self._level] == 0).item()
        if not check:
            raise AssertionError("The level must be 0 at the root.")
        
        root_right = data.loc[sel, self._right]
        target_right = 2 * data.shape[0]
        if (root_right != target_right).item():
            msg = f"The root has right value of {root_right}, it should be {target_right}."
            raise AssertionError(msg)