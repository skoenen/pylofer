from storage import Storage

from sqlalchemy import create_engine

class SQLAlchemyStorage(Storage):
    def __init__(self, config={}, data=None):
        self.db_uri = getattr(config, "storage.uri")
        self.engine = create_engine(getattr)
