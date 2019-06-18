import logging
import uuid
from threading import Thread
from model_buyer.exceptions.exceptions import OrderedModelNotFoundException
from model_buyer.model.ordered_model import OrderedModel, OrderedModelStatus
from model_buyer.service.federated_trainer_connector import FederatedTrainerConnector
import numpy as np

from model_buyer.utils.singleton import Singleton


class ModelBuyer(metaclass=Singleton):

    def __init__(self):
        self.id = None
        self.encryption_service = None
        self.data_loader = None
        self.config = None
        self.federated_trainer_connector = None
        self.models = None
        self.predictions = None

    def init(self, encryption_service, data_loader, config):
        self.id = str(uuid.uuid1())
        self.encryption_service = encryption_service
        self.data_loader = data_loader
        self.config = config
        if config:
            self.federated_trainer_connector = FederatedTrainerConnector(config)
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
        X_test, y_test = self.data_loader.get_sub_set()
        model = OrderedModel(data_requirements, model_type, X_test)
        model.request_data = dict(requirements=requirements,
                                  model_id=model.id,
                                  model_buyer_id=self.id,
                                  weights=model.get_weights(),
                                  public_key=self.encryption_service.get_public_key(),
                                  test_data=[X_test.tolist(), y_test.tolist()])
        self.federated_trainer_connector.send_model_order(model.request_data)
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
        return self._update_model(model_id, data, OrderedModelStatus.IN_PROGRESS)

    def _update_model(self, model_id, data, status):
        weights = self.encryption_service.decrypt_and_deserizalize_collection(
            self.encryption_service.get_private_key(),
            data['model']
        ) if self.config["ACTIVE_ENCRYPTION"] else data['model']
        model = self.get_model(model_id)
        model.set_weights(np.asarray(weights))
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
        # TODO: Check this x_test
        x_test, y_test = self.data_loader.get_sub_set()
        prediction = model.predict(x_test, y_test)
        prediction.model = model
        self.predictions.add(prediction)
        return prediction

    def get_prediction(self, prediction_id):
        return next(filter(lambda x: x.id == prediction_id, self.predictions), None)

    def transform_prediction(self, prediction_data):
        """
       {'model_id': self.model_id,
        'prediction_id': self.id,
        'encrypted_prediction': Data Owner encrypted prediction,
        'public_key': Data Owner PK}
       :param prediction_data:
       :return:
       """
        decrypted_prediction = self.encryption_service.decrypt_collection(prediction_data["encrypted_prediction"])
        encrypted_to_data_owner = self.encryption_service.encrypt_collection(decrypted_prediction,
                                                                             public_key=prediction_data["public_key"])
        prediction_transformed = {
            "encrypted_prediction": encrypted_to_data_owner,
            "model_id": prediction_data["model_id"],
            "prediction_id": prediction_data["prediction_id"]
        }
        Thread(target=self.federated_trainer_connector.send_transformed_prediction,
               args=prediction_transformed).start()
