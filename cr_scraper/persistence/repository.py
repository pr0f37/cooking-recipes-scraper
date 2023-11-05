from abc import ABC, abstractmethod
from contextlib import ContextDecorator
from typing import Self
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, registry

from cr_scraper.persistence.db_engine import engine
from cr_scraper.persistence.mapper import mapper_registry


class Repository(ABC, ContextDecorator):
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get():
        raise NotImplementedError

    @abstractmethod
    def save():
        raise NotImplementedError

    @abstractmethod
    def delete():
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

    def get(self, model, id: UUID | None = None):
        if id:
            return self.session.scalar(select(model).where(model.id == id))
        return [elem for elem in self.session.scalars(select(model)).all()]

    def save(self, model) -> None:
        self.session.add(model)

    def delete(self) -> None:
        pass

    def commit(self) -> None:
        self.session.commit()
