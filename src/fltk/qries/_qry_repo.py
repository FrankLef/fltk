import duckdb as ddb


class QryRepo:
    def __init__(self, conn: ddb.DuckDBPyConnection, table_nm: str):
        self.conn = conn
        self.table_nm = table_nm
