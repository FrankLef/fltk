from ._qry_repo import QryRepo


class QryUpdate(QryRepo):
    def write_add_col(self, col: str, dtype: str) -> str:
        qry: str = (
            f"ALTER TABLE {self.table_nm} ADD COLUMN IF NOT EXISTS {col} {dtype};"
        )
        return qry

    def write_update(self, col: str, upd_text: str) -> str:
        qry: str = f"UPDATE {self.table_nm} SET {col} = {upd_text}"
        return qry

    def write_update_from(
        self,
        col: str,
        upd_text: str,
        from_table: str,
        join_vars: tuple[str, str],
    ) -> str:
        if from_table == self.table_nm:
            msg: str = f"Main table and From table must have different name. They both have the name '{self.table_nm}'."
            raise ValueError(msg)
        qry: str = f"""
        UPDATE {self.table_nm} SET {col} = {upd_text}
        FROM {from_table}
        WHERE {self.table_nm}.{join_vars[0]} = {from_table}.{join_vars[1]};
        """
        return qry

    def add_cols(self, cols: dict[str, str]) -> None:
        """_summary_

        Args:
            cols (dict[str, str]): _description_
        """
        for name, dtype in cols.items():
            qry_add = self.write_add_col(col=name, dtype=dtype)
            self.conn.sql(qry_add)

    def update(self, col: str, upd_text: str) -> None:
        qry_update = self.write_update(col=col, upd_text=upd_text)
        self.conn.sql(qry_update)

    def update_from(
        self, col: str, upd_text: str, from_table: str, join_vars: tuple[str, str]
    ) -> None:
        """Update a table using values from a reference table.

        Args:
            col (str): Name of column to update.
            upd_text (str): Text to describle the update to apply on `col`.
            from_table (str): Name of reference table.
            join_vars (tuple[str, str]): The name of the 2 columns, first column for the table, second for the reference table.
        """
        qry_update_from = self.write_update_from(
            col=col, upd_text=upd_text, from_table=from_table, join_vars=join_vars
        )
        # print("qry_update_from:\n", qry_update_from)
        # raise KeyboardInterrupt()
        self.conn.sql(qry_update_from)

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
