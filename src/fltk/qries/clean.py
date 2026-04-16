from ._qry_repo import QryRepo


class QryClean(QryRepo):
    @property
    def table_nm(self) -> str:
        return self._table_nm

    def clean_ws(self, col: str) -> None:
        """Remove leading and trailing white spaces and replace multiple whitespaces.

        Including white space but also tab, linefeed, etc.

        Args:
            col (str): Column name.
        """
        pats = ((r"^\s+|\s$", ""), (r"[\t\n\r\v\f]+", ""), (r" +", " "))
        for pat, replace in pats:
            qry = f"""
            UPDATE {self.table_nm}
            SET {col} = regexp_replace({col}, '{pat}', '{replace}', 'g')
            WHERE {col} IS NOT NULL;
            """
            self._conn.sql(qry)
