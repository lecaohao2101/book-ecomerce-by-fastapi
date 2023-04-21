from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class CategoryModel(Base):
    name: Mapped[str] = mapped_column(
        String
    )
    list_book: Mapped[list["BookModel"]] = relationship(
        back_populates="category", lazy="subquery")

    def __str__(self):
        return f'{self.name}'