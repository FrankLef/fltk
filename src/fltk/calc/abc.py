from abc import ABC, abstractmethod
from pathlib import Path

class Calc(ABC):
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        summary = self.get_summary()
        title = f"{type(self).__name__}: {self.name}"
        out = title + "\n" + ("-" * len(title)) + "\n"
        for key, value in summary.items():
            out += f"{key:<10}: {value}\n"
        return out
    
    @abstractmethod
    def fit(self, *args, **kwargs):
        """Fit process."""
        pass
    
    @abstractmethod
    def transform(self, *args, **kwargs):
        """Fit process."""
        pass

    @abstractmethod
    def get_summary(self) -> dict[str, tuple[int, ...]]:
        """Define summary string used by __repr__"""
        pass
    
    @abstractmethod
    def to_excel(self, path: Path) -> None:
        """Export data to excel."""
        pass