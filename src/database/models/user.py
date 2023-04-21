from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base_class import Base
from src.database.models import *


class UserModel(Base):
    email: Mapped[str] = mapped_column(
        String(length=100), unique=True
    )
    full_name: Mapped[str] = mapped_column(
        String(length=100)
    )
    password: Mapped[str] = mapped_column(
        String(length=20)
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("role.id")
    )
    role: Mapped["RoleModel"] = relationship(
        "RoleModel", lazy="subquery"
    )
    list_address: Mapped[list["AddressModel"]] = relationship(
        back_populates="user", lazy="subquery"
    )
    list_order: Mapped[list["OrderModel"]] = relationship(
        back_populates="user", lazy="subquery"
    )
    list_store: Mapped[list["StoreModel"]] = relationship(
        back_populates="user", lazy="subquery"
    )

    def __str__(self):
        return f'{self.full_name}'