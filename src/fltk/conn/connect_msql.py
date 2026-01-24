"""Instantiate a connection to a MS SQL database."""

import sqlalchemy as sa
from typing import NamedTuple
import pandas as pd


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
    # Since version 1.4.17 sqlalchemy requires a sqlalchemy.engine.url.URL to create the engine.
    # We can't use just a string anymore.
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
    an_engine = sa.create_engine(engine_url)
    return an_engine


def test_connect(engin: sa.Engine) -> bool:
    try:
        with engin.connect() as conn:
            out = conn.execute(sa.text("SELECT 1"))
            for row in out:
                print(row)
    except sa.exc.InterfaceError as e:
        msg = f"CONNECTION FAILED:\n{e}"
        print(msg)
        raise e
    finally:
        engin.dispose()
    return True


def fetch(qry: str) -> pd.DataFrame:
    engin = build_engine(
        driver_nm=params.driver_nm,
        driver=params.driver,
        server=params.server,
        database=params.database,
        user=params.user,
        pw=params.pw,
        port=params.port,
    )
    try:
        with engin.connect() as conn:
            data = pd.read_sql_query(sql=sa.text(qry), con=conn)
    except sa.exc.InterfaceError as e:
        msg = f"CONNECTION FAILED:\n{e}"
        print(msg)
        raise e
    finally:
        engin.dispose()
    return data


def main(test_it: bool = False) -> sa.Engine:
    engin = build_engine(
        driver_nm=params.driver_nm,
        driver=params.driver,
        server=params.server,
        database=params.database,
        user=params.user,
        pw=params.pw,
        port=params.port,
    )
    if test_it:
        test_connect(engin)
    return engin
