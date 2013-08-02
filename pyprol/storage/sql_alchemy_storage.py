from pyprol.storage import Storage

from sqlalchemy import create_engine

SCHEME = ["sqlite", "mysql", "postgresql", "oracle", "mssql+pyodbc"]

class SQLAlchemyStorage(Storage):
    def __init__(self, config={}):
        self.db_uri = getattr(config, "storage_endpoint")
        self.engine = create_engine(getattr)
