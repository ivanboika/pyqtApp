from sqlalchemy.orm import DeclarativeBase
import abc


class Base(DeclarativeBase):
    @abc.abstractmethod
    def getPrimaryKey(self):
        pass

    @abc.abstractmethod
    def toList(self) -> []:
        pass