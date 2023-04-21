from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base_class import Base


class CategoryRequest(Base):
    name: Mapped[str] = mapped_column(
        String
    )
    description: Mapped[str] = mapped_column(
        String
    )
    status: Mapped[str] = mapped_column(
        Boolean, server_default="0"
    )
    store_owner_id: Mapped[str] = mapped_column(
        String
    )
    def __str__(self):
        return f'{self.name}{self.status}'