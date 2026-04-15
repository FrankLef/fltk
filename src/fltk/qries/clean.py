import duckdb as ddb


class QryClean:
    def __init__(self, conn: ddb.DuckDBPyConnection, table_nm: str):
        self._conn = conn
        self._table_nm = table_nm

    @property
    def table_nm(self) -> str:
        return self._table_nm

    def clean_ws(self, col: str) -> None:
        """Remove leading and trailing white spaces and replace multiple whitespaces.

        Including white space but also tab, linefeed, etc. See Python docs.
        """

        # \s include white space but also tab, linefeed, etc. See Python docs.

        pats = {r"^\s+|\s$": "", r"[\t\n\r\v\f]+": "", r" +": " "}
        for pat, replace in pats.items():
            qry = f"""
            UPDATE {self.table_nm}
            SET {col} = regexp_replace({col}, '{pat}', '{replace}', 'g')
            WHERE {col} IS NOT NULL;
            """
            self._conn.sql(qry)
