# includes all responses from UI
from sqlalchemy import create_engine, select, inspect
from sqlalchemy import MetaData
from src.DBAccess.config import connStrForSQLAlchemy
from sqlalchemy.orm import Session
from src.Model.BaseModel import Base


class Controller:
    def __init__(self):
        self.engine = create_engine(connStrForSQLAlchemy)

    def getDataFromTable(self, table: Base):
        data = []
        with Session(self.engine) as session:
            stmt = select(Base)
            for chair in session.scalars(stmt):
                data.append(chair.toList())
        return data

    def getAllTableNames(self) -> list[str]:
        metadata = MetaData()
        metadata.reflect(self.engine)

        return metadata.tables.keys()

    def insertData(self, item: Base):
        pass

    def getColumnNames(self, table: str) -> list[str]:
        pass
