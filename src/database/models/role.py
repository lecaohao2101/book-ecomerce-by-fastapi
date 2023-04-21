from enum import Enum
from sqlalchemy import Enum as EnumColumn
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base_class import Base


class RoleEnum(Enum):
    ADMIN = 'ADMIN'
    STORE_OWNER = 'STORE_OWNER'
    CUSTOMER = 'CUSTOMER'


class RoleModel(Base):
    name: Mapped[str] = mapped_column(
        EnumColumn(RoleEnum), server_default=RoleEnum.CUSTOMER.value
    )

    def __str__(self):
        return f'{self.name.value}'