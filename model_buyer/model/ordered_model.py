import uuid
import numpy as np
from commons.model.model_service import ModelFactory
from enum import Enum


class OrderedModelStatus(Enum):
    INITIATED = 1
    IN_PROGRESS = 2
    FINISHED = 3


class OrderedModel:

    def __init__(self, requirements, model_type, data):
        self.id = str(uuid.uuid1())
        self.model_type = model_type
        self.requirements = requirements
        self.model = ModelFactory.get_model(model_type)(data)
        self.request_data = None
        self.status = OrderedModelStatus.INITIATED

    def set_weights(self, weights):
        self.model.set_weights(weights)

    def predict(self, x, y):
        x_array = np.asarray(x)
        y_array = np.asarray(y)
        return self.model.predict(x, y)

    def get_weights(self):
        return self.model.weights.tolist()




