import logging
import uuid

import numpy as np

from commons.decorators.decorators import optimized_collection_parameter
from commons.model.model_service import ModelFactory
from data_owner.service.federated_trainer_connector import FederatedTrainerConnector
from data_owner.service.prediction_service import PredictionService


class DataOwner:

    def __init__(self, config, data_loader, encryption_service):
        """
        :param config:
        :param data_loader:
        :param encryption_service:
        """

        self.client_id = str(uuid.uuid1())
        self.client_name = "data_owner {}".format(self.client_id)
        self.config = config
        self.data_loader = data_loader
        self.register_number = None
        self.model = None
        self.trainings = {}
        self.encryption_service = encryption_service
        self.federated_trainer_connector = FederatedTrainerConnector(self.config)
        self.prediction_service = PredictionService(self.encryption_service)
        if config['REGISTRATION_ENABLE']:
            self.register()

    def process(self, model_type, public_key):
        """
        Process to run model
        :param model_type:
        :param public_key:
        :return:
        """
        self.encryption_service.set_public_key(public_key)
        X, y = self.data_loader.get_sub_set()
        self.model = self.model if self.model else ModelFactory.get_model(model_type)(X, y)
        return self.model.compute_gradient().tolist()

    def register(self):
        """
        Register client into federated server
        :return:
        """
        response = self.federated_trainer_connector.register(self._get_register_data())
        self.register_number = int(response['data_owner_id'])
        logging.info("Register Number" + str(self.register_number))

    def _get_register_data(self):
        return {'id': self.client_id}

    def get_data_owner_register_number(self):
        return self.register_number

    def get_model(self):
        return self.model.weights.tolist()

    def link_dataset_to_training_request(self, training_request_id, requirements):
        filename = self.data_loader.get_dataset_for_training(requirements)
        self.trainings[training_request_id] = filename
        self.data_loader.load_data(filename)
        return filename is not None

    @optimized_collection_parameter(optimization=np.asarray, active=True)
    def step(self, step_data):
        """
        TODO: POdría evaluarse la posibilidad de que el federated trainer indique cuando evaluar una prediccion local
        :param encrypted_model:
        :return:
        """
        self.model.gradient_step(step_data, float(self.config['ETA']))
        if False:
            y_test = [] # TODO: De donde sale esto??
            prediction = self.model.predict(self.model.X, y_test)
            # model_public_key
            model_public_key = None
            model_id = self.model.id
            self._evaluate_prediction(prediction, model_id, model_public_key)

    def _evaluate_prediction(self, encrypted_prediction, model_id, model_public_key):
        """
        prediction: values + model_buyer_id

        :param encrypted_prediction:
        :return:
        """
        prediction_data = {
            "linked_model": self.model,
            "encrypted_prediction": encrypted_prediction,
            "model": {
                "public_key": model_public_key,
                "id": model_id
            }
        }
        # Model + PK Model owner
        prediction = self.prediction_service.add(prediction_data)
        self.federated_trainer_connector.send_prediction(prediction)

    def get_predictions(self):
        return self.prediction_service.get()

    def get_prediction(self, prediction_id):
        return self.prediction_service.get(prediction_id)

    def check_prediction_consistency(self, prediction_id, prediction_data):
        return self.prediction_service.check_consistency(prediction_id, prediction_data)


class DataOwnerFactory:
    @classmethod
    def create_data_owner(cls, name, data_loader, encryption_service):
        """
        :param name:
        :param data_loader:
        :param encryption_service:
        :return:
        """
        return DataOwner(name, data_loader, encryption_service)
