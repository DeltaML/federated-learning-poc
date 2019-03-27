from enum import Enum

from commons.model.linear_regression import LinearRegression


class ModelType(Enum):
    LINEAR_REGRESSION = 1

    @classmethod
    def validate(cls, model_type):
        return any(model_type == item.name for item in cls)


class ModelFactory:

    @classmethod
    def get_model(cls, model_type):
        if ModelType[model_type] == ModelType.LINEAR_REGRESSION:
            return LinearRegression
        else:
            raise ValueError(model_type)
