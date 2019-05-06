import uuid
import logging
import requests

from commons.data.data_loader import DataLoader
from model_buyer.model.ordered_model import OrderedModel


class ModelBuyer:
    def __init__(self, public_key, private_key, encryption_service, config):
        self.id = str(uuid.uuid1())
        self.public_key = public_key
        self.private_key = private_key
        self.encryption_service = encryption_service
        self.config = config
        #TODO: refactor this to DB
        self.models = set()
        self.predictions = set()

    def make_new_order_model(self, order_data):
        """

        :param order_data:
        :return:
        """
        model = OrderedModel(order_data)
        data = dict(type=model.model_type,
                    call_back_port=self.config["port"],
                    model_id=model.id,
                    public_key=self.public_key.n)
        response = requests.post(self.config["server_register_url"], json=data)
        response.raise_for_status()
        model.request_data = data
        self.models.add(model)

    def update_model(self, model_id, data):
        """

        :param model_id:
        :param data:
        :return:
        """
        d_data = self.encryption_service.decrypt_and_deserizalize_collection(self.private_key, data) if self.config[
            "active_encryption"] else data
        logging.info("DATA {}".format(d_data))
        self.get_model(model_id).set_weights(d_data)

    def get_model(self, model_id):
        return next(filter(lambda x: x.id == model_id, self.models), None)

    def make_prediction(self, data):
        """

        :param data:
        :return:
        """
        model_id = data["model_id"]
        X_train, y_train, X_test, y_test = DataLoader().load_random_data()
        prediction = self.get_model(model_id).predict(X_test)
        self.predictions.add(prediction)
        return prediction

    def get_prediction(self, prediction_id):
        return next(filter(lambda x: x.id == prediction_id, self.predictions), None)





