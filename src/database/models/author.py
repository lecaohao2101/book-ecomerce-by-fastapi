from typing import List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class AuthorModel(Base):
    name: Mapped[str] = mapped_column(
        String
    )
    image: Mapped[str] = mapped_column(
        String, nullable=True
    )
    description: Mapped[str] = mapped_column(
        String, nullable=True
    )
    books: Mapped[List["BookModel"]] = relationship(
        back_populates="author"
    )
    def __str__(self):
        return f'{self.name}'