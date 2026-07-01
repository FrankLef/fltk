from abc import ABC, abstractmethod


class DiczBase(ABC):
    def __repr__(self) -> str:
        msg: str = "\n".join([key + ": " + str(val) for key, val in self.info.items()])
        return msg

    @property
    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def append(self, *args, **kwargs):
        """Append new element to collection.."""
        pass
