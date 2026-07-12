import duckdb as ddb
from duckdb.sqltypes import DOUBLE

from ._qry_repo import QryRepo
from .log1ps import log1ps10, expm1s10


class QryTransformLog(QryRepo):
    def add(self, col: str) -> str:
        qry: str = f"ALTER TABLE {self.table_nm} ADD COLUMN IF NOT EXISTS {col} FLOAT;"
        return qry

    def create_log1ps10_fn(self, conn: ddb.DuckDBPyConnection) -> None:
        try:
            conn.create_function(
                name="log1ps10",
                function=log1ps10,
                parameters=[DOUBLE],
                return_type=DOUBLE,
            )
        except ddb.NotImplementedException:
            pass  # function already exists, skip it.

    def create_expm1s10_fn(self, conn: ddb.DuckDBPyConnection) -> None:
        try:
            conn.create_function(
                name="expm1s10",
                function=expm1s10,
                parameters=[DOUBLE],
                return_type=DOUBLE,
            )
        except ddb.NotImplementedException:
            pass  # function already exists, skip it.

    def transform(self, num_var: str, log_var: str) -> None:
        self.create_log1ps10_fn(self.conn)
        qry = self.add(col=log_var)
        self.conn.sql(qry)
        qry = f"UPDATE {self.table_nm} SET {log_var} = log1ps10({num_var});"
        self.conn.sql(qry)

    def inverse(self, num_var: str, exp_var: str) -> None:
        self.create_expm1s10_fn(self.conn)
        qry = self.add(col=exp_var)
        self.conn.sql(qry)
        qry = f"UPDATE {self.table_nm} SET {num_var} = expm1s10({exp_var});"
        self.conn.sql(qry)
