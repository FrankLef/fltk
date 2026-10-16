from abc import ABC, abstractmethod
import sqlalchemy as sa
import polars as pl


class ConnectMsql(ABC):
    """Connection to a MS SQL database."""

    def __init__(self) -> None:
        self._engine = self._build_engine()

    @property
    def engine(self):
        return self._engine

    @abstractmethod
    def _build_engine(self) -> sa.Engine:
        pass

    def test_connect(self) -> bool:
        """Test the MS SQL engine."""
        conn: sa.engine.Connection = self._engine.connect()
        try:
            out = conn.execute(sa.text("SELECT 1"))
            for row in out:
                print(row)
        except sa.exc.InterfaceError as e:
            e.add_note(f"CONNECTION FAILED:\n{e}")
            raise
        return True

    def fetch(self, qry: str) -> pl.DataFrame:
        """Fetch data from MS SQL database using polars."""
        conn: sa.engine.Connection = self._engine.connect()
        try:
            data = pl.read_database(sa.text(qry), connection=conn)
        except sa.exc.InterfaceError as e:
            e.add_note(f"CONNECTION FAILED:\n{e}")
            raise
        return data
