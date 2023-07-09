from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    CRUD operations for the User model.
    """

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Retrieves a user by their email.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `email`: The email of the user.

        #### Returns

        * An instance of the User model if found, otherwise None.
        """
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Creates a new user.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `obj_in`: The input data for creating the user.

        #### Returns

        * An instance of the created User model.
        """
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password.get_secret_value()),
            roleID=obj_in.roleID,
            enabled=obj_in.enabled,
            institution_id=obj_in.institution_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Updates a user.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `db_obj`: The existing user object to be updated.
        * `obj_in`: The input data for updating the user.

        #### Returns

        * An instance of the updated User model.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(
                update_data["password"].get_secret_value()
            )
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Authenticates a user.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `email`: The email of the user.
        * `password`: The password of the user.

        #### Returns

        * An instance of the authenticated User model if successful, otherwise None.
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """
        Checks if a user is active.

        #### Parameters

        * `user`: The User instance.

        #### Returns

        * True if the user is active, False otherwise.
        """
        return user.enabled

    def is_superuser(self, user: User) -> bool:
        """
        Checks if a user is a superuser.

        #### Parameters

        * `user`: The User instance.

        #### Returns

        * True if the user is a superuser, False otherwise."""
        return True if user.roleID == "SuperAdmin" else False

    def has_admin_privilege(self, user: User) -> bool:
        """
        Checks if a user has admin privileges.

        #### Parameters

        * `user`: The User instance.

        #### Returns

        * True if the user has admin privileges, False otherwise.
        """
        return True if user.roleID in ("SuperAdmin", "Admin") else False


user = CRUDUser(User)
