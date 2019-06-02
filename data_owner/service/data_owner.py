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
        self.encryption_service = encryption_service
        self.register_number = None
        self.model = None
        self.trainings = {}
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
        self.register_number = int(response['number']) - 1
        logging.info("Register Number" + str(self.register_number))

    def _get_register_data(self):
        return {'id': self.client_id}

    @optimized_collection_parameter(optimization=np.asarray, active=True)
    def step(self, step_data):
        """
        TODO: POdría evaluarse la posibilidad de que el federated trainer indique cuando evaluar una prediccion local
        :param encrypted_model:
        :return:
        """
        self.model.gradient_step(step_data["gradient"], float(self.config['ETA']))
        if step_data["evaluate_model"]:
            y_test = [] # TODO: De donde sale esto??
            prediction = self.model.predict(self.model.X, y_test)
            self._evaluate_prediction(prediction)

    def get_data_owner_register_number(self):
        return self.register_number

    def get_model(self):
        return self.model.weights.tolist()

    def link_dataset_to_training_request(self, training_request_id, requirements):
        filename = self.data_loader.get_dataset_for_training(requirements)
        self.trainings[training_request_id] = filename
        self.data_loader.load_data(filename)
        return filename is not None

    def _evaluate_prediction(self, prediction_request):
        """
        prediction: values + model_buyer_id

        :param prediction_request:
        :return:
        """
        prediction_data = {
            "encrypted_prediction": prediction_request,
            "public_key": self.encryption_service.get_public_key(),
        }
        # Model +  PK Model owner
        self.prediction_service.add(prediction_request)
        self.federated_trainer_connector.send_prediction(prediction_data)

    def get_predictions(self):
        return self.prediction_service.get()

    def get_prediction(self, prediction_id):
        return self.prediction_service.get(prediction_id)

    def check_prediction_consistency(self, prediction_id, prediction_data):
        self.prediction_service.check_consistency(prediction_id, prediction_data)


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
