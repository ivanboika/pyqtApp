from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import create_engine, select, inspect
from src.Model.BaseModel import Base
from sqlalchemy import MetaData


class Chair(Base):
    __tablename__ = 'chairs'

    article: Mapped[str] = mapped_column(primary_key=True, __name_pos='article')
    name: Mapped[str] = mapped_column()
    amount: Mapped[int] = mapped_column()
    producer: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Chair(article={self.article!r}," \
               f" name={self.name!r}, amount={self.amount!r}, producer={self.producer!r}, photo={self.photo!r})"

    def toList(self) -> list:
        return [self.article, self.name, self.amount, self.producer, self.photo]


if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://postgres:1221909128@localhost/app')
    session = Session(engine)

    stmt = select(Chair)

    insp = inspect(Chair)

    metadata = MetaData()
    metadata.reflect(engine)

    for table in metadata.tables.keys():
        print(table)



    for item in insp.columns:
        print(item.name)

    for chair in session.scalars(stmt):
        print(chair)
