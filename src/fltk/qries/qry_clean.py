import duckdb as ddb
import string


class QryClean:
    def __init__(self, conn: ddb.DuckDBPyConnection, table_nm: str):
        self._conn = conn
        self._table_nm = table_nm

    @property
    def table_nm(self) -> str:
        return self._table_nm

    def clean_ws(self, col: str) -> None:
        qry = f"""
        UPDATE {self.table_nm}
        SET {col} = trim({col}, '{string.whitespace}')
        WHERE {col} IS NOT NULL;
        """
        self._conn.sql(qry)

        qry = f"""
        UPDATE {self.table_nm}
        SET {col} = regexp_replace({col}, '\s+', ' ','g')
        WHERE {col} IS NOT NULL;
        """
        self._conn.sql(qry)
