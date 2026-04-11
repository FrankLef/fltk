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
        """Remove extra white spaces."""
        qry = f"""
        UPDATE {self.table_nm}
        SET {col} = trim({col}, '{string.whitespace}')
        WHERE {col} IS NOT NULL;
        """
        self._conn.sql(qry)

        qry = f"""
        UPDATE {self.table_nm}
        SET {col} = regexp_replace({col}, r"\s+", ' ','g')
        WHERE {col} IS NOT NULL;
        """
        self._conn.sql(qry)

    def clean_nonprint(self, col: str) -> None:
        """Remove non-printable characters."""
        rgx = r"[[:cntrl:]]"  # all non-printable ASCII (0-31, 127)
        qry = f"""
        UPDATE {self.table_nm}
        SET {col} = regexp_replace({col}, '{rgx}', '','g')
        WHERE {col} IS NOT NULL;
        """
        self._conn.sql(qry)

        #  any character that is not a printable character, tab, carriage return, or newline.
        rgx = r"[^[:print:]\t\r\n]"
        qry = f"""
        UPDATE {self.table_nm}
        SET {col} = regexp_replace({col}, '{rgx}', '','g')
        WHERE {col} IS NOT NULL;
        """
        self._conn.sql(qry)
