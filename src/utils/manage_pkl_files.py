import pickle
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Callable, Union

# from phase2_module.src.utils.provide import classproperty
from provide import classproperty


BASE: Path = Path(Path(__file__).resolve().parent.parent.parent, "pkls")


class PickleManager:
    @classproperty
    def metadata_directory(self) -> List[str]:
        """
        needs data preprocessing class pickle directory names
        exclude: models, params
        return: List[str] -> [country, customer ...]
        """
        ignore = ["models", "params"]

        return [_file for _file in os.listdir(BASE) if _file not in ignore]

    def save(directory: str, name: str, pkl_file, prefix=None):
        """
        directory: pickle save into directory name
        name: pickle save file name
        prefix: [default] None -> pickle name combine prefix string
        """
        save_directory = Path(BASE, directory)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        file_name_format = f'{name}_{prefix}.pickle'

        file_save_path = Path(BASE, directory, file_name_format)

        with open(file_save_path, 'wb') as file:
            pickle.dump(pkl_file, file)

    @classmethod
    def load(cls,  pkl_type: str, pkl_name: str) -> Dict[str, Union[str, Dict]]:
        """
        if you need get only one pickle file.

        pkl_type: where is in directory e.g) country, model, customer ...
        pkl_name: for load pickle file name
        """
        pkl_path = Path(BASE, pkl_type, f"{pkl_name}.pickle")

        with open(pkl_path, 'rb') as f:
            data = pickle.load(f)

        return data

    @classmethod
    def loads(cls, directory: str) -> List[Dict]:
        """
        if you need get a lot of pickle file.
        directory: exists pickle file directory name
        """
        parameter_pkl: Dict[Dict] = defaultdict(dict)

        for _file in os.listdir(Path(BASE, directory)):
            if _file.endswith(".pickle"):
                pkl_name = _file.split(".")[0]
                pkl_path = Path(BASE, directory, _file)

                with open(pkl_path, "rb") as pkl_file:
                    parameter_pkl[directory][pkl_name] = pickle.load(pkl_file)
        return parameter_pkl

    @classmethod
    def map(cls, function: Callable, datas: List[str]) -> Dict[str, Union[str, Dict]]:
        """
        built-in map function customizing.
        function: function object id
        datas: list types data
        return: returns to dictionary data
        """

        result = {}

        for data in map(PickleManager.loads, PickleManager.metadata_directory):
            result.update(data)

        return result


if __name__ == "__main__":
    print(PickleManager.metadata_directory)
    print(PickleManager.map(PickleManager.loads, PickleManager.metadata_directory).get("customer"))
    print(PickleManager.load("test", "test_mode"))
