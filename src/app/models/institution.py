from typing import Optional
from sqlalchemy import BigInteger, String, Text, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base_class import Base


class Institution(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    contactno: Mapped[str] = mapped_column(String(10), nullable=False)

    membership: Mapped[Optional[int]]
