from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class AuthorModel(Base):
    name: Mapped[str] = mapped_column(
        String
    )

    book: Mapped["BookModel"] = relationship(
        "BookModel", lazy="subquery", back_populates="list_book_author"
    )
    def __str__(self):
        return f'{self.name}'