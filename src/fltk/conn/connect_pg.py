"""Connect to PostgreSQL database."""

from typing import NamedTuple
from sqlalchemy import create_engine, URL
from sqlalchemy.engine.base import Engine  # for type hint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session  # for type hint
from sqlalchemy_utils import database_exists

# source: https://www.youtube.com/watch?v=neW9Y9xh4jc
# source: https://docs.sqlalchemy.org/en/20/orm/session_basics.html


class ConnParams(NamedTuple):
    driver_nm: str
    database: str
    user: str
    pw: str
    host: str
    port: int


params = ConnParams(
    driver_nm="postgresql+psycopg2",
    database="tuba_skinny",
    user="postgres",
    pw="p@ssword",
    host="localhost",
    port=5432,
)


def get_engine(
    driver: str,
    db: str,
    user: str,
    passwd: str,
    host: str,
    port: int,
) -> Engine:
    """Create an sqlalchemy engine for postgreSQL."""
    # NOTE: You MUST use parse.quote_plus from urllib to avoid problem with the password when it contains characters such as '@' which creates an invalid url.
    # passwd = quote_plus(passwd)
    # url = rf"{driver}://{user}:{passwd}@{host}:{port}/{db}"
    url = URL.create(
        drivername=driver,
        username=user,
        password=passwd,
        host=host,
        port=port,
        database=db,
    )
    if not database_exists(url):
        raise FileExistsError(f"Invalid database url\n{url}")
    engine = create_engine(url=url, pool_size=50, echo=False)
    return engine


def main() -> Session:
    """Create an sqlalchemy session for postgreSQL."""
    engine = get_engine(
        driver=params.driver_nm,
        db=params.database,
        user=params.user,
        passwd=params.pw,
        host=params.host,
        port=params.port,
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    engine.dispose()
    return session


if __name__ == "__main__":
    main()
