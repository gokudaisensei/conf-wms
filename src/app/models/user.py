from sqlalchemy import BigInteger, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional

from app.models.institution import Institution
from app.db.base_class import Base


class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    contactno: Mapped[str] = mapped_column(String(15), unique=True)
    title: Mapped[Optional[Enum]] = mapped_column(Enum("Mr.", "Ms.", "Mrs.", "Dr."))
    department: Mapped[Optional[str]] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Optional[Enum]] = mapped_column(
        Enum(
            "SuperAdmin",
            "Admin",
            "Coordinator",
            "Editor",
            "AssociateEditor",
            "Reviewer",
            "Author",
        )
    )
    institution_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey(Institution.__tablename__ + ".id")
    )
    enabled: Mapped[bool] = mapped_column(default=False)

    institution: Mapped["Institution"] = relationship("Institution", backref="users")
