from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd

from ..utils import to_excel as xl


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

    @property
    @abstractmethod
    def dfs(self) -> dict[str, pd.DataFrame]:
        """Dictionnary of dataframes."""
        pass

    def get_summary(self) -> dict[str, tuple[int, ...]]:
        """Create summary of dataframes."""
        summary = {key: df.shape for key, df in self.dfs.items()}
        return summary

    def to_excel(self, path: Path) -> None:
        """Export dataframes to excel. Usually for debug."""
        name = f"{type(self).__name__} '{self.name}'"
        xl.to_excel(name, path=path, dfs=self.dfs)
