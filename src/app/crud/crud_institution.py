from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.institution import Institution
from app.models.user import User
from app.schemas.institution import InstitutionCreate, InstitutionUpdate


class CRUDInstitution(CRUDBase[Institution, InstitutionCreate, InstitutionUpdate]):
    """
    CRUD operations for the Institution model.
    """

    def get_by_name(self, db: Session, *, name: str) -> Institution | None:
        """
        Retrieves an institution by its name.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `name`: The name of the institution.

        #### Returns

        * An instance of the Institution model if found, otherwise None.
        """
        return db.query(Institution).filter(Institution.name == name).first()

    def get_multi_user(
        self, db: Session, *, id: int, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """
        Retrieves multiple users associated with an institution.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `id`: The ID of the institution.
        * `skip`: The number of users to skip (for pagination).
        * `limit`: The maximum number of users to retrieve.

        #### Returns

        * A list of User instances associated with the institution.
        """
        institution = self.get(db, id=id)
        return institution.users[skip : skip + limit]


institution = CRUDInstitution(Institution)
