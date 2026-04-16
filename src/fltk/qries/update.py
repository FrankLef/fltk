from ._qry_repo import QryRepo


class QryUpdate(QryRepo):
    @property
    def table_nm(self) -> str:
        return self._table_nm

    def write_add_col(self, col: str, dtype: str) -> str:
        qry: str = (
            f"ALTER TABLE {self._table_nm} ADD COLUMN IF NOT EXISTS {col} {dtype};"
        )
        return qry

    def write_update(self, col: str, upd_text: str) -> str:
        qry: str = f"UPDATE {self._table_nm} SET {col} = {upd_text}"
        return qry

    def write_update_from(
        self,
        col: str,
        upd_text: str,
        from_table: str,
        join_vars: tuple[str, str],
    ) -> str:
        if from_table == self._table_nm:
            msg: str = f"Main table and From table must have different name. They both have the name '{self._table_nm}'."
            raise ValueError(msg)
        qry: str = f"""
        UPDATE {self._table_nm} SET {col} = {upd_text}
        FROM {from_table}
        WHERE {self._table_nm}.{join_vars[0]} = {from_table}.{join_vars[1]};
        """
        return qry

    def add_cols(self, cols: dict[str, str]) -> None:
        for name, dtype in cols.items():
            qry_add = self.write_add_col(col=name, dtype=dtype)
            self._conn.sql(qry_add)

    def update(self, col: str, upd_text: str) -> None:
        qry_update = self.write_update(col=col, upd_text=upd_text)
        self._conn.sql(qry_update)

    def update_from(
        self, col: str, upd_text: str, from_table: str, join_vars: tuple[str, str]
    ) -> None:
        qry_update_from = self.write_update_from(
            col=col, upd_text=upd_text, from_table=from_table, join_vars=join_vars
        )
        # print("qry_update_from:\n", qry_update_from)
        # raise KeyboardInterrupt()
        self._conn.sql(qry_update_from)

    def add_update(self, col: str, dtype: str, upd_text: str) -> None:
        self.add_cols({col: dtype})
        self.update(col=col, upd_text=upd_text)

    def add_update_from(
        self,
        col: str,
        dtype: str,
        upd_text: str,
        from_table: str,
        join_vars: tuple[str, str],
    ) -> None:
        self.add_cols({col: dtype})
        self.update_from(
            col=col, upd_text=upd_text, from_table=from_table, join_vars=join_vars
        )
