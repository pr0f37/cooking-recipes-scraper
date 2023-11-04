from abc import ABC, abstractmethod


class Repository(ABC):
    def __init__(self, model) -> None:
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
