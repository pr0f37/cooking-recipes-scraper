from abc import ABC, abstractmethod
from contextlib import ContextDecorator
from typing import Self
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, registry

from cr_scraper.persistence.db_engine import engine
from cr_scraper.persistence.mapper import mapper_registry


class Repository(ABC, ContextDecorator):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, *exc) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self, model, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add(self, model):
        raise NotImplementedError

    @abstractmethod
    def save(self, *args):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args):
        raise NotImplementedError


class SQLRepository(Repository):
    def __init__(
        self, engine: Engine = engine, registry: registry = mapper_registry
    ) -> None:
        self.registry = registry
        self.engine = engine

    def __enter__(self) -> Self:
        self.session = Session(self.engine)
        return self

    def __exit__(self, *exc) -> bool:
        self.session.close()
        return False

    def get(self, model, **kwargs):
        # id: UUID | None = None):
        name = kwargs.get("name")
        id = kwargs.get("id")
        if isinstance(name, str):
            db_model = [
                elem
                for elem in self.session.scalars(
                    select(model).where(model.name.ilike(f"%{name}%"))
                ).all()
            ]
            if not db_model:
                raise NotExistInRepositoryError
            return db_model
        if isinstance(id, UUID):
            db_model = self.session.scalar(select(model).where(model.id == id))
            if db_model is None:
                raise NotExistInRepositoryError
            return db_model
        return [elem for elem in self.session.scalars(select(model)).all()]

    def add(self, model) -> None:
        self.session.add(model)

    def save(self) -> None:
        self.session.commit()

    def delete(self, model) -> None:
        self.session.delete(model)


class NotExistInRepositoryError(Exception):
    """
    Element does not exist in the repository
    """

    def __init__(self, *args: object) -> None:
        super().__init__("Element does not exist in the repository", *args)
