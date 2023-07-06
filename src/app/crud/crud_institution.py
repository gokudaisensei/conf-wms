from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.institution import Institution
from app.schemas.institution import (
    InstitutionCreate,
    InstitutionUpdate,
)


class CRUDInstitution(CRUDBase[Institution, InstitutionCreate, InstitutionUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Institution | None:
        return db.query(Institution).filter(Institution.name == name).first()

    def get_multi_user(self, db: Session, *, id: int, skip: int = 0, limit: int = 100):
        institution = self.get(db, id=id)
        return institution.users[skip : skip + limit]


institution = CRUDInstitution(Institution)
