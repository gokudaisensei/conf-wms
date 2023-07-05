import datetime
from sqlalchemy import BigInteger, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, and_
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.associationproxy import association_proxy
from typing import List, Optional

from app.db.base_class import Base


class Institution(Base):
    id: Mapped[int] = mapped_column(BigInteger,
                                               primary_key=True, autoincrement=True)
    institutionName: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    institutionAddress: Mapped[str] = mapped_column(Text, nullable=False)
    emailID: Mapped[str] = mapped_column(String(255), nullable=False)
    contactNum: Mapped[str] = mapped_column(String(10), nullable=False)
    membership: Mapped[Enum] = mapped_column(
        Enum('Choice1', 'Choice2'), nullable=False)
