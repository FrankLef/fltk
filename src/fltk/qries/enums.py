from .base import QryRepo


class QryEnums(QryRepo):
    def create_enum_by_sum(self, enum_nm: str, col: str, size_col: str) -> None:
        qry = f"DROP TYPE IF EXISTS {enum_nm}"
        self.conn.sql(qry)

        qry = f"""
            CREATE TYPE {enum_nm} AS ENUM
            (
            WITH tmp AS
                (
                SELECT {col}, sum({size_col}) AS tot
                FROM {self.table_nm} GROUP BY {col}
                )
            SELECT {col} FROM tmp ORDER BY tot DESC
            )
            """
        self.conn.sql(qry)

    def apply_enum(self, enum_nm: str, col: str) -> None:
        qry = f"""
        ALTER TABLE {self.table_nm} ALTER COLUMN {col} TYPE {enum_nm};
        """
        self.conn.sql(qry)

    def get_enums(self, enum_nm: str) -> list:
        qry = f"SELECT enum_range(NULL::{enum_nm})"
        enums = self.conn.sql(qry).fetchone()[0]  # type: ignore
        return enums
