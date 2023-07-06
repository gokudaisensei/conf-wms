from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for performing CRUD operations on a SQLAlchemy model.

    #### Parameters

    * `ModelType`: The SQLAlchemy model type.
    * `CreateSchemaType`: The Pydantic model type for create operations.
    * `UpdateSchemaType`: The Pydantic model type for update operations.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initializes the CRUD object with the provided SQLAlchemy model.

        #### Parameters

        * `model`: A SQLAlchemy model class.
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Retrieves a single model instance by its ID.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `id`: The ID of the model instance to retrieve.

        #### Returns

        * An optional instance of the model if found, otherwise None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieves multiple instances of the model.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `skip`: The number of instances to skip (for pagination).
        * `limit`: The maximum number of instances to retrieve.

        #### Returns

        * A list of model instances.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Creates a new model instance.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `obj_in`: The input data for creating the model instance.

        #### Returns

        * The created model instance.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Updates an existing model instance.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `db_obj`: The existing model instance to update.
        * `obj_in`: The input data for updating the model instance.

        #### Returns

        * The updated model instance.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType | None:
        """
        Removes a model instance by its ID.

        #### Parameters

        * `db`: The SQLAlchemy database session.
        * `id`: The ID of the model instance to remove.

        #### Returns

        * The removed model instance if found, otherwise None.
        """
        if not (obj := db.query(self.model).get(id)):
            return None
        db.delete(obj)
        db.commit()
        return obj
