import logging
import uuid

import requests

from commons.data.data_loader import DataLoader
from model_buyer.exceptions.exceptions import OrderedModelNotFoundException
from model_buyer.model.ordered_model import OrderedModel, OrderedModelStatus


class ModelBuyer:
    def __init__(self, public_key, private_key, encryption_service, data_loader, config):
        self.id = str(uuid.uuid1())
        self.public_key = public_key
        self.private_key = private_key
        self.encryption_service = encryption_service
        self.data_loader = data_loader
        self.config = config
        # TODO: refactor this to DB
        self.models = set()
        self.predictions = set()

    def make_new_order_model(self, requirements):
        """

        :param requirements:
        :return:
        """
        data_requirements = requirements["data_requirements"]
        model_type = requirements["model_type"]
        model = OrderedModel(data_requirements, model_type)
        data = dict(requirements=requirements,
                    model_id=model.id,
                    public_key=self.public_key.n)
        requests.post(self.config["server_register_url"], json=data).raise_for_status()
        model.request_data = data
        self.models.add(model)
        return {"requirements": model.requirements,
                "model": {"id": model.id,
                          "status": model.status.name,
                          "type": model.model_type,
                          "weights": model.get_weights()
                          }
                }

    def finish_model(self, model_id, data):
        model = self._update_model(model_id, data, OrderedModelStatus.FINISHED)
        logging.info("Model status: {} weights {}".format(model.status.name, model.get_weights()))

    def update_model(self, model_id, data):
        """

        :param model_id:
        :param data:
        :return:
        """
        self._update_model(model_id, data, OrderedModelStatus.IN_PROGRESS)

    def _update_model(self, model_id, data, status):
        weights = self.encryption_service.decrypt_and_deserizalize_collection(self.private_key, data) if self.config[
            "active_encryption"] else data
        model = self.get_model(model_id)
        model.set_weights(weights)
        model.status = status
        return model

    def get_model(self, model_id):
        return next(filter(lambda x: x.id == model_id, self.models), None)

    def make_prediction(self, data):
        """

        :param data:
        :return:
        """
        model_id = data["model_id"]
        model = self.get_model(model_id)
        if not model:
            raise OrderedModelNotFoundException(model_id)

        x_test, y_test = self.data_loader.get_sub_set()
        prediction = model.predict(x_test, y_test)
        prediction.model = model
        self.predictions.add(prediction)
        return prediction

    def get_prediction(self, prediction_id):
        return next(filter(lambda x: x.id == prediction_id, self.predictions), None)
