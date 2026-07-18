from abc import ABC, abstractmethod


class DiczBase(ABC):
    def __init__(self, key: str) -> None:
        self.key: str = key

    def __repr__(self) -> str:
        title = f"{type(self).__name__}: {self.key}"
        msg = title + "\n" + ("-" * len(title)) + "\n"
        for key, value in self.info.items():
            msg += f"{key:<10}: {str(value)}\n"
        return msg

    @property
    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def append(self, *args, **kwargs):
        """Append new element to collection."""
        pass
