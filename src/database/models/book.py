from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class BookModel(Base):
    image: Mapped[str] = mapped_column(
        String
    )
    name: Mapped[str] = mapped_column(
        String
    )
    description: Mapped[str] = mapped_column(
        String
    )
    price: Mapped[str] = mapped_column(
        Float
    )
    stock: Mapped[str] = mapped_column(
        Integer
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id")
    )
    store_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("store.id")
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("author.id")
    )
    store: Mapped["StoreModel"] = relationship(
        "StoreModel", lazy="subquery", back_populates="list_book"
    )
    category: Mapped["CategoryModel"] = relationship(
        "CategoryModel", lazy="subquery", back_populates="list_book"
    )
    list_book_order_item: Mapped["OrderItemModel"] = relationship(
         lazy="subquery", back_populates="book"
    )
    list_book_author: Mapped["AuthorModel"] = relationship(
         "AuthorModel", lazy="subquery", back_populates="book"
    )

    def __str__(self):
        return f'{self.name}'