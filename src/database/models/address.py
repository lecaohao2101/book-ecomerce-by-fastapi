from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_class import Base


class AddressModel(Base):
    country: Mapped[str] = mapped_column(
        String
    )
    city: Mapped[str] = mapped_column(
        String
    )
    district: Mapped[str] = mapped_column(
        String
    )
    ward: Mapped[str] = mapped_column(
        String
    )
    street: Mapped[str] = mapped_column(
        String
    )
    number_home: Mapped[str] = mapped_column(
        String
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id")
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", lazy="subquery", back_populates="list_address"
    )

    def __str__(self):
        return f'{self.number_home} {self.street}, {self.district}, {self.city}, {self.country}'