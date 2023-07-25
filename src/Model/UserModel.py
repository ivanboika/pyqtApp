from src.Model.BaseModel import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'

    login: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    passhash: Mapped[str] = mapped_column()
    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"User(login = {self.login!r}, email = {self.email!r}, passhash = {self.passhash!r}, id = {self.id!r}))"

    def toList(self) -> list:
        return [self.login, self.email, self.passhash, self.id]
