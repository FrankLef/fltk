# ruff: noqa: C408

"""Instantiate a MS SQL engine with trusted connection.."""

from typing import NamedTuple

import polars as pl
import sqlalchemy as sa

# EXAMPLE HOW TO USE
# def main():
#     engine = get_engine()
#     with engine.connect() as conn:
#         test_connect(conn)


class ConnParams(NamedTuple):
    driver_nm: str
    driver: str  # must match name in odbc list from windows
    server: str
    database: str
    Trusted_Connection: str
    port: int = 1433  # optional, 1433 is the default


params = ConnParams(
    driver_nm="mssql+pyodbc",
    driver="SQL Server",
    server=r"jrysvrsql01\bi_data_wh",
    database="BI_SJM_TEST",
    Trusted_Connection="yes",
    port=1433,
)


def build_engine(
    driver_nm: str,
    driver: str,
    server: str,
    database: str,
    trusted_conn: str = "yes",
    port: int = 1433,
) -> sa.Engine:
    """Create a MS SQL engine with trusted connection."""

    # NOTE: Since version 1.4.17 sqlalchemy requires a sqlalchemy.engine.url.URL to create the engine.
    # NOTE: You MUST use parse.quote_plus from urllib to avoid problem with the password when it contains characters such as '@' which creates an invalid url.
    # passwd = quote_plus(passwd)
    # url = rf"{driver}://{user}:{passwd}@{host}:{port}/{db}"
    engine_url = sa.engine.url.URL.create(
        drivername=driver_nm,
        host=server,
        database=database,
        port=port,
        query=dict(trusted_connection=trusted_conn, driver=driver),
    )
    # NOTE: Debug line to see the connection string
    # print("connection string:", engine_url.render_as_string(), "\n", sep="\n")
    an_engine = sa.create_engine(engine_url)
    return an_engine


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
        trusted_conn=params.Trusted_Connection,
        port=params.port,
    )
    return engine
