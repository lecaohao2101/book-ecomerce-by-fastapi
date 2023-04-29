from sqlalchemy import Integer, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class OrderModel(Base):
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id")
    )
    total: Mapped[str] = mapped_column(
        Float
    )
    status: Mapped[bool] = mapped_column(
        Boolean, server_default="0"
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", lazy="subquery", back_populates="list_order"
    )
    list_order_item:Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order"
    )

    def __str__(self):
        return f'{self.id}'