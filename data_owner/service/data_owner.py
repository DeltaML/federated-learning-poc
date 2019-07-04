import logging
import uuid

import numpy as np

from commons.decorators.decorators import optimized_collection_parameter
from commons.model.model_service import ModelFactory
from data_owner.service.federated_trainer_connector import FederatedTrainerConnector


class DataOwner:

    def __init__(self, config, data_loader):
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
        self.federated_trainer_connector = FederatedTrainerConnector(self.config)
        if config['REGISTRATION_ENABLE']:
            self.register()

    def train(self, model_type, weights):
        X, y = self.data_loader.get_sub_set()
        self.model = self.model if self.model else ModelFactory.get_model(model_type)(X, y)
        self.model.set_weights(weights)
        gradient = self.model.fit(10, self.config['ETA'])
        return self.client_id, gradient.tolist()

    def process(self, model_type, weights):
        """
        Process to run model
        :param model_type:
        :param weights:
        :return:
        """
        logging.info("Initializing local model")
        X, y = self.data_loader.get_sub_set()
        self.model = self.model if self.model else ModelFactory.get_model(model_type)(X, y)
        self.model.set_weights(weights)
        return self.client_id, self.model.compute_gradient().tolist()

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

    def link_dataset_to_model_id(self, training_request_id, requirements):
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
        logging.info("Model current weights {}".format(self.model.weights.tolist()))

    def model_quality_metrics(self, model_type, weights):
        """
        Method used only by validator role. It doesn't use the model built from the data. It gets the model from
        the federated trainer and use the local data to calculate quality metrics
        :return: the model quality (currently measured with the MSE)
        """
        X_test, y_test = self.data_loader.get_sub_set()
        self.model = self.model if self.model else ModelFactory.get_model(model_type)()
        self.model.set_weights(weights)
        mse = self.model.predict(X_test, y_test).mse
        logging.info("Calculated mse: {}".format(mse))
        return mse


class DataOwnerFactory:
    @classmethod
    def create_data_owner(cls, name, data_loader):
        """
        :param name:
        :param data_loader:
        :return:
        """
        return DataOwner(name, data_loader)
