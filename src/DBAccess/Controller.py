# includes all responses from UI
from sqlalchemy import create_engine, select, inspect, insert
from sqlalchemy import MetaData
from src.DBAccess.config import connStrForSQLAlchemy
from sqlalchemy.orm import Session
from src.Model.BaseModel import Base
from src.Model.ChairModel import Chair


class Controller:
    def __init__(self):
        self.engine = create_engine(connStrForSQLAlchemy)

    def getDataFromTable(self, table: Base):
        data = []
        with Session(self.engine) as session:
            stmt = select(table)
            for item in session.scalars(stmt):
                data.append(item.toList())
        return data

    def getAllTableNames(self) -> list[str]:
        metadata = MetaData()
        metadata.reflect(self.engine)

        return metadata.tables.keys()

    def insertData(self, table: Base, values):
        with Session(self.engine) as session:
            session.execute(insert(table), values)
            session.commit()

    def getColumnNames(self, table: Base) -> list[str]:
        columns = []
        insp = inspect(table)
        for item in insp.columns:
            columns.append(item.name)
        return columns


if __name__ == '__main__':
    con = Controller()
    print(con.getDataFromTable(Chair))
