from abc import ABC, abstractmethod

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session, registry

from cr_scraper.persistence.mapper import mapper_registry

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/cr-scraper", echo=True
)


class Repository(ABC):
    def __init__(self) -> None:
        super().__init__()

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
    def __init__(self, engine: Engine, registry: registry = mapper_registry) -> None:
        self.registry = registry
        self.engine = engine

    def get(self, model):
        with Session(self.engine) as session:
            return session.execute(select(model)).all()

    def save(self, model) -> None:
        with Session(self.engine) as session:
            session.add(model)
            session.commit()

    def delete(self) -> None:
        pass
