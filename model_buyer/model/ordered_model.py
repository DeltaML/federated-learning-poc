import uuid

from commons.model.model_service import ModelFactory


class OrderedModel:
    def __init__(self, model_type="LINEAR_REGRESSION"):
        self.id = str(uuid.uuid1())
        self.model_type = model_type
        self.weights = []
        self.model = ModelFactory.get_model(model_type)()
        self.request_data = None
