from sqlalchemy.orm import Mapped, mapped_column, Session
from src.Model.BaseModel import Base


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

    def getPrimaryKey(self):
        return self.article

