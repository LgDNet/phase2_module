from dataclasses import dataclass
import pandas as pd
from pathlib import Path


BASE = Path(__file__).resolve().parent


class classproperty:  # noqa
    def __init__(self, method):
        self.func = method

    def __get__(self, instance, cls):
        return self.func(cls)


@dataclass
class Data:
    _train: str = Path(BASE, "train.csv")
    _submission: str = Path(BASE, "test.csv")

    @classproperty
    def train(self):
        return pd.read_csv(self._train)

    @classproperty
    def submission(self):
        return pd.read_csv(self._submission)


if __name__ == "__main__":
    print(Data._train)
    print(Data._test)
    print(Data._submission)
