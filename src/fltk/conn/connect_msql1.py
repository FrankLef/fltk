"""Instantiate a connection to a MS SQL database."""

import sqlalchemy as sa
from typing import NamedTuple
import polars as pl


class ConnParams(NamedTuple):
    driver_nm: str
    driver: str  # must match name in odbc list from windows
    server: str
    database: str
    user: str
    pw: str
    port: int = 1433  # optional, 1433 is the default


params = ConnParams(
    driver_nm="mssql+pyodbc",
    driver="SQL Server",
    server="azuohsqlbi01.database.windows.net",
    database="olivahorti_bi_db1",
    user="flefebvreodbc",
    pw="Excursion-Companion-Squad3!",
    port=1433,
)


def build_engine(
    driver_nm: str,
    driver: str,
    server: str,
    database: str,
    user: str,
    pw: str,
    port: int = 1433,
) -> sa.Engine:
    # NOTE: Since version 1.4.17 sqlalchemy requires a sqlalchemy.engine.url.URL to create the engine.
    # NOTE: You MUST use parse.quote_plus from urllib to avoid problem with the password when it contains characters such as '@' which creates an invalid url.
    # passwd = quote_plus(passwd)
    # url = rf"{driver}://{user}:{passwd}@{host}:{port}/{db}"
    engine_url = sa.engine.url.URL.create(
        drivername=driver_nm,
        username=user,
        password=pw,
        host=server,
        port=port,
        database=database,
        query=dict(driver=driver),
    )
    # NOTE: Debug line to see the connection string
    # print("connection string:", engine_url.render_as_string(), "\n", sep="\n")
    engine = sa.create_engine(engine_url)
    return engine


def test_connect(conn: sa.orm.session.Session) -> bool:
    """Test the MS SQL engine."""
    try:
        out = conn.execute(sa.text("SELECT 1"))
        for row in out:
            print(row)
    except sa.exc.InterfaceError as e:
        e.add_note(f"CONNECTION FAILED:\n{e}")
        raise
    return True


def fetch(conn: sa.orm.session.Session, qry: str) -> pl.DataFrame:
    """Fetch data from MS SQL database using polars."""
    try:
        data = pl.read_database(sa.text(qry), connection=conn)
    except sa.exc.InterfaceError as e:
        e.add_note(f"CONNECTION FAILED:\n{e}")
        raise
    return data


def main() -> sa.Engine:
    engine = build_engine(
        driver_nm=params.driver_nm,
        driver=params.driver,
        server=params.server,
        database=params.database,
        user=params.user,
        pw=params.pw,
        port=params.port,
    )
    return engine
