from ._qry_repo import QryRepo


class QryInfo(QryRepo):
    def count(self, where_txt: str | None = None) -> int:
        if where_txt is None:
            qry = f"SELECT count(*) FROM {self.table_nm};"
        else:
            qry = f"SELECT count(*) FROM {self.table_nm} WHERE {where_txt};"
        nrows: int = int(self.conn.sql(qry).fetchone()[0])  # type: ignore
        return nrows

    def assert_empty(self, msg: str | None = None) -> bool:
        qry: str = f"FROM {self.table_nm} LIMIT 1;"
        check: int = len(self.conn.sql(qry).fetchone())  # type: ignore
        if not check:
            if msg is None:
                msg = f"'{self.table_nm}' is empty."
            raise AssertionError(msg)
        return False
