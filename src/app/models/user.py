import datetime
from sqlalchemy import BigInteger, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, and_
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.associationproxy import association_proxy
from typing import List, Optional

from app.models.institution import Institution
from app.db.base_class import Base

class User(Base):
    id: Mapped[int] = mapped_column(BigInteger,
                                               primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(
        String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    roleID: Mapped[Optional[Enum]] = mapped_column(
        Enum(
            'SuperAdmin',
            'Admin',
            'Coordinator',
            'Editor',
            'AssociateEditor',
            'Reviewer',
            'Author'
        )
    )
    institution_id: Mapped[Optional[int]] = mapped_column(BigInteger,
                                                         ForeignKey(Institution.__tablename__ + ".id"))
    enabled: Mapped[bool] = mapped_column(default=False)

    institution: Mapped["Institution"] = relationship(
        "Institution", backref="users")