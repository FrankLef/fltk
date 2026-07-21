from abc import ABC, abstractmethod
from enum import StrEnum, auto


type DiczNames = tuple[str, ...]


class DiczVar(StrEnum):
    GROUP = auto()
    LINE = auto()
    SKIPPED = auto()
    ROLE = auto()
    RULE = auto()


class DiczBase(ABC):
    def __init__(self, name: str) -> None:
        self.name: str = name

    # def __repr__(self) -> str:
    #     title = f"{type(self).__name__}: {self.name}"
    #     msg = title + "\n" + ("-" * len(title)) + "\n"
    #     for key, value in self.info.items():
    #         msg += f"{key}: {str(value)}\n"
    #     return msg

    @property
    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def append(self, *args, **kwargs):
        """Append new element to collection."""
        pass
