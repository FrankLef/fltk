import sqlalchemy as sa
from .connect_msql_base import ConnectMsql


class ConnectMsqlTrusted(ConnectMsql):
    """Connection to a MS SQL database with trusted connection.

    This class has an engine build with trusted connection.
    """

    def __init__(
        self,
        server: str,
        database: str,
        *,
        trusted_conn: str = "yes",
        driver="SQL Server",
        driver_name: str = "mssql+pyodbc",
        port: int = 1433,
    ):
        self._server = server
        self._database = database
        self._trusted_conn = trusted_conn
        self._driver = driver
        self._driver_name = driver_name
        self._port = port
        self._engine = self._build_engine()

    def _build_engine(self) -> sa.Engine:
        # NOTE: Since version 1.4.17 sqlalchemy requires a sqlalchemy.engine.url.URL to create the engine.
        # NOTE: You MUST use parse.quote_plus from urllib to avoid problem with the password when it contains characters such as '@' which creates an invalid url.
        # passwd = quote_plus(passwd)
        # url = rf"{driver}://{user}:{passwd}@{host}:{port}/{db}"
        engine_url = sa.engine.url.URL.create(
            drivername=self._driver_name,
            host=self._server,
            database=self._database,
            port=self._port,
            query=dict(trusted_connection=self._trusted_conn, driver=self._driver),
        )
        # NOTE: Debug line to see the connection string
        # print("connection string:", engine_url.render_as_string(), "\n", sep="\n")
        engine = sa.create_engine(engine_url)
        return engine
