from typing import Sequence

from ._qry_repo import QryRepo


class QryClean(QryRepo):
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
            self.conn.sql(qry)

    def drop_cols(self, cols: Sequence[str]) -> None:
        for col in cols:
            qry: str = f"ALTER TABLE {self.table_nm} DROP COLUMN {col};"
            self.conn.sql(qry)

    def ren_cols(self, cols: dict[str, str]) -> None:
        for old_nm, new_nm in cols.items():
            qry = f"ALTER TABLE {self.table_nm} RENAME {old_nm} TO {new_nm};"
            self.conn.sql(qry)

    def reorder_cols(self, schema_cols: Sequence[str]) -> None:
        qry: str = f"SELECT column_name FROM (DESCRIBE {self.table_nm});"
        describe_cols = self.conn.sql(qry).fetchall()
        table_cols = [col[0] for col in describe_cols]
        missed_cols = [col for col in table_cols if col not in schema_cols]
        ordered_cols = [col for col in schema_cols if col in table_cols]
        select_cols = ordered_cols + missed_cols
        select_csv = ",".join(select_cols)
        qry = f"""
        CREATE OR REPLACE TABLE {self.table_nm} AS
        SELECT {select_csv} FROM {self.table_nm};
        """
        self.conn.sql(qry)
