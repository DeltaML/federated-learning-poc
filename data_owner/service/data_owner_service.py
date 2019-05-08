import logging
import uuid

import numpy as np

from commons.decorators.decorators import optimized_collection_parameter
from commons.model.model_service import ModelFactory
from data_owner.service.federated_trainer_connector import FederatedTrainerConnector


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
        #X, y = self.data_loader.get_sub_set(self.get_data_owner_register_number())
        X, y = self.data_loader.get_sub_set()
        self.model = self.model if self.model else ModelFactory.get_model(model_type)(X, y)
        return self.model.compute_gradient().tolist()

    def register(self):
        """
        Register client into federated server
        :return:
        """
        response = FederatedTrainerConnector(self.config).register(self._get_register_data())
        self.register_number = int(response['number']) - 1
        logging.info("Register Number" + str(self.register_number))

    def _get_register_data(self):
        return {'id': self.client_id}

    @optimized_collection_parameter(optimization=np.asarray, active=True)
    def step(self, encrypted_model):
        self.model.gradient_step(encrypted_model, float(self.config['ETA']))

    def get_data_owner_register_number(self):
        return self.register_number

    def get_model(self):
        return self.model.weights.tolist()

    def link_dataset_to_trainig_request(self, training_request_id, requeriments):
        filename = self.data_loader.get_dataset_for_training(requeriments)
        self.trainings[training_request_id] = filename
        self.data_loader.load_data(filename)
        return filename

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
