from sqlalchemy import Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class OrderModel(Base):
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id")
    )
    created_date: Mapped[str] = mapped_column(
        DateTime
    )
    total: Mapped[str] = mapped_column(
        Float
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", lazy="subquery", back_populates="list_order"
    )
    list_order_item:Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order", lazy="subquery"
    )

    def __str__(self):
        return f'{self.id}'