from enum import Enum

from commons.model.exceptions.exceptions import InvalidModelException
from commons.model.linear_regression import LinearRegression


class ModelType(Enum):
    LINEAR_REGRESSION = 1

    @classmethod
    def validate(cls, model_type):
        if not any(model_type == item.name for item in cls):
            raise InvalidModelException(model_type)


class ModelFactory:

    @classmethod
    def get_model(cls, model_type):
        if ModelType[model_type] == ModelType.LINEAR_REGRESSION:
            return LinearRegression
        else:
            raise InvalidModelException(model_type)
