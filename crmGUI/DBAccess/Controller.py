# includes all responses from UI
from sqlalchemy import create_engine, select, inspect, insert, update
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from crmGUI.Model.BaseModel import Base
from crmGUI.DBAccess.config import connStrForSQLAlchemy
from crmGUI.DBAccess.config import dockerURL
import regex as rgx


# it should be like restapi
class Controller:
    def __init__(self):
        self.engine = create_engine(dockerURL)

    def getDataFromTable(self, table: Base):
        data = []
        with Session(self.engine) as session:
            stmt = select(table)
            for item in session.scalars(stmt):
                try:
                    data.append(item.toList())
                except AttributeError:
                    pass
                finally:
                    print('No items')

        return data

    def getAllTableNames(self) -> list[str]:
        metadata = MetaData()
        metadata.reflect(self.engine)

        return metadata.tables.keys()

    def insertRecord(self, table: Base, values):
        with Session(self.engine) as session:
            session.execute(insert(table), values)
            session.commit()

    def getColumnNames(self, table: Base) -> list[str]:
        columns = []
        if type(table) is None:
            insp = inspect(table)
            for item in insp.columns:
                columns.append(item.name)
        return columns

    def updateRecord(self, table: Base, values):
        primaryKey = rgx.split('(.+)[.](.+)$', table.getPrimaryKey(table).__str__())[2]

        primaryItem = values.pop(primaryKey)
        with Session(self.engine) as session:
            session.execute(update(table).where(table.getPrimaryKey(table) == primaryItem), values)
            session.commit()
