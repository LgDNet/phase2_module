from dataclasses import dataclass
import pandas as pd
from pathlib import Path

from src.utils.provide import classproperty


BASE = Path(Path(__file__).resolve().parent.parent.parent, "data")


@dataclass
class Data:
    _train: str = Path(BASE, "train.csv")
    _test: str = Path(BASE, "test.csv")

    @classproperty
    def train(self):
        return pd.read_csv(self._train)

    @classproperty
    def test(self):
        return pd.read_csv(self._test)


if __name__ == "__main__":
    print(Data._train)
    print(Data._test)
