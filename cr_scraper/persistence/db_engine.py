import os

from sqlalchemy import Engine, create_engine

DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "cr-scraper")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


class DBEngine:
    @staticmethod
    def init(
        db_host: str = DB_HOST,
        db_port: str = DB_PORT,
        db_name: str = DB_NAME,
        db_user: str = DB_USER,
        db_password: str = DB_PASSWORD,
    ) -> Engine:
        dialect = "postgresql+psycopg2"
        return create_engine(
            f"{dialect}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )


engine = DBEngine.init()
