from sqlalchemy import String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class OrderItemModel(Base):
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("book.id")
    )
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("order.id")
    )
    quantity: Mapped[str] = mapped_column(
        Integer
    )
    subtotal: Mapped[str] = mapped_column(
        Float
    )
    order: Mapped["OrderModel"] = relationship(
        "OrderModel", lazy="subquery", back_populates="list_order_item"
    )
    book: Mapped["BookModel"] = relationship(
        "BookModel", lazy="subquery", back_populates="list_book_order_item"
    )

    def __str__(self):
        return f'{self.book.name} {self.quantity}'