import logging
import os
import uuid
from threading import Thread

import numpy as np

from commons.model.model_service import ModelFactory
from model_buyer.exceptions.exceptions import OrderedModelNotFoundException
from model_buyer.model.buyer_model import BuyerModel, BuyerModelStatus
from model_buyer.service.federated_trainer_connector import FederatedTrainerConnector
from model_buyer.utils.singleton import Singleton


class ModelBuyer(metaclass=Singleton):

    def __init__(self):
        self.id = str(uuid.uuid1())
        self.encryption_service = None
        self.data_loader = None
        self.config = None
        self.federated_trainer_connector = None

    def init(self, encryption_service, data_loader, config):
        self.encryption_service = encryption_service
        self.data_loader = data_loader
        self.config = config
        if config:
            self.federated_trainer_connector = FederatedTrainerConnector(config)

    def all(self):
        return BuyerModel.get()

    def make_new_order_model(self, requirements):
        """

        :param requirements:
        :return:
        """
        data_requirements = requirements["data_requirements"]
        model_type = requirements["model_type"]
        file_name = requirements["testing_file_name"]
        self.data_loader.load_data(file_name)
        x_test, y_test = self.data_loader.get_sub_set()
        ordered_model = BuyerModel(model_type=model_type, data=x_test)
        ordered_model.requirements = data_requirements
        ordered_model.request_data = dict(requirements=requirements,
                                          model_id=ordered_model.id,
                                          model_buyer_id=self.id,
                                          weights=ordered_model.model.weights.tolist(),
                                          test_data=[x_test.tolist(), y_test.tolist()])
        ordered_model.save()

        self.federated_trainer_connector.send_model_order(ordered_model.request_data)
        return {"requirements": ordered_model.requirements,
                "model": {"id": ordered_model.id,
                          "status": ordered_model.status,
                          "type": ordered_model.model_type,
                          "weights": ordered_model.model['weights']
                          }
                }

    def finish_model(self, model_id, data):
        buyer_model = self._update_model(model_id, data, BuyerModelStatus.FINISHED.name)
        logging.info("Model status: {} weights {}".format(buyer_model.status, buyer_model.model["weights"]))

    def update_model(self, model_id, data):
        """

        :param model_id:
        :param data:
        :return:
        """
        return self._update_model(model_id, data, BuyerModelStatus.IN_PROGRESS.name)

    def _update_model(self, model_id, data, status):
        weights = self.encryption_service.decrypt_and_deserizalize_collection(
            self.encryption_service.get_private_key(),
            data['model']
        ) if self.config["ACTIVE_ENCRYPTION"] else data['model']
        ordered_model = self.get(model_id)
        model = ModelFactory.load_model(ordered_model.model_type, ordered_model.model)
        model.set_weights(np.asarray(weights))
        ordered_model.model = model
        ordered_model.status = status
        ordered_model.save()
        return ordered_model

    def get(self, model_id):
        return BuyerModel.get(model_id)

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

    def load_data_set(self, file, filename):
        logging.info(file)
        file.save(os.path.join(self.config.get("DATA_SETS_DIR"), filename))
        file.close()
