import json

from sklearn.model_selection import train_test_split
from src.utils.top_score_instance import check_the_score
import optuna
from optuna.samplers import TPESampler
from pathlib import Path

BASE = Path(__file__).parent
DATA = None


def set_params_optimization_data(x, y):
    global DATA

    DATA = train_test_split(x, y, test_size=0.1, random_state=42, stratify=y)
    return DATA


def load_schema(schema_name: str):
    """
    schema_name: Model name types has str
    """
    schema_path = Path(BASE, "schema", f"{schema_name}.json")

    try:
        with open(schema_path, "r") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"load schema in error: {e}")

    return schema


def display_best_param_score(study_best_trial):
    """
    Optuna의 최적화 된 파라미터 결과 확인

    study_best_trial: study.best_trial
    """
    print('Best trial:')
    print('  Value: ', study_best_trial.value)
    print('  Params: ')
    for key, value in study_best_trial.params.items():
        print(f'{key}: {value}')


def xgboost_opt(model):
    """
    model: Model instance
    schema_name: Schema file name
    """

    schema = load_schema("xgboost")

    x_train, x_test, y_train, y_test = DATA
    evals = [(x_test, y_test)]

    def objective(trial):
        param = {}
        for parameter_name, parameter_info in schema.items():
            if parameter_info.get("dtype") == "int":
                param[parameter_name] = trial.suggest_int(parameter_name, *parameter_info.get("params"))
                continue
            param[parameter_name] = trial.suggest_float(parameter_name, *parameter_info.get("params"))

        xgbopt = model.set_params(**param, )
        xgbopt.fit(x_train, y_train)  # TODO: 추가 인자 적용 하기
        preds = xgbopt.predict(x_test)
        accuracy = check_the_score(y_test, preds).get("f1")  # NOTE: XGBoost는 스코어 한 개만 추출 해서 리턴해야함
        return accuracy

    study = optuna.create_study(study_name="xgboost", direction='maximize')
    study.optimize(objective, n_trials=1, timeout=5000)

    l_trial = study.best_trial
    display_best_param_score(l_trial)

    return l_trial.params


def lightgbm_opt(model):
    """
    model: Model instance
    schema_name: Schema file name
    """
    schema = load_schema("lightgbm")

    def objective(trial):
        x_train, x_test, y_train, y_test = DATA
        evals=[(x_test, y_test)]

        data_types_option = {
            "int": lambda param_name, param_info: trial.suggest_int(param_name, *param_info.get("params")),
            "var": lambda _, __, : len(set(y_train)),
            "float": lambda param_name, param_info: trial.suggest_float(param_name, *param_info.get("params")),
            "str": lambda _, param_info: param_info.get("params"),
        }
        data_types = list(data_types_option.keys())

        param = {}
        for parameter_name, parameter_info in schema.items():
            for dtype in data_types:
                if parameter_info.get("dtype") == dtype:
                    method = data_types_option.get(dtype)
                    param[parameter_name] = method(parameter_name, parameter_info)

        gbm = model.set_params(**param)
        gbm.fit(x_train, y_train)
        preds = gbm.predict(x_test)
        accuracy = check_the_score(y_test, preds)
        return accuracy

    sampler = TPESampler(seed=1)
    study = optuna.create_study(study_name="lightgbm", direction="maximize", sampler=sampler)
    study.optimize(objective, n_trials=1, timeout=2000)

    l_trial = study.best_trial
    display_best_param_score(l_trial)

    return l_trial.params
