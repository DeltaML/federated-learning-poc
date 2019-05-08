import logging
import requests
import json
from functools import reduce
from threading import Thread

from commons.decorators.decorators import normalize_optimized_response
from commons.operations_utils.functions import sum_collection
from federated_trainer.models.data_owner_instance import DataOwnerInstance
from federated_trainer.service.data_owner_connector import DataOwnerConnector
from federated_trainer.service.decorators import serialize_encrypted_server_data
from federated_trainer.service.model_buyer_connector import ModelBuyerConnector


class FederatedTrainer:
    def __init__(self, encryption_service, config):
        self.data_owners = []
        self.encryption_service = encryption_service
        self.config = config
        self.active_encryption = self.config["ACTIVE_ENCRYPTION"]
        self.data_owner_connector = DataOwnerConnector(self.config["DATA_OWNER_PORT"], encryption_service, self.active_encryption)
        self.model_buyer_connector = ModelBuyerConnector(self.config["MODEL_BUYER_PORT"])

    def register_data_owner(self, data_owner_data):
        """
        Register new data_owner
        :param data_owner_data:
        :return:
        """

        logging.info("Register data owner with {}".format(data_owner_data))
        new_data_owner = DataOwnerInstance(data_owner_data)
        self.data_owners.append(new_data_owner)
        return {'number': len(self.data_owners)}

    def send_requirements_to_data_owner(self, data):
        self.data_owner_connector.send_requirements_to_data_owners(self.data_owners, data)

    def async_server_processing(self, remote_address, model_id, func, *args):
        logging.info("process_in_background...")
        self.model_buyer_connector.set_remote_buyer_data(remote_address, model_id)
        result = func(*args)
        self.model_buyer_connector.send_result(result)

    def process(self, remote_address, data):
        Thread(target=self.async_server_processing, args=self._build_async_processing_data(data, remote_address)).start()

    def _build_async_processing_data(self, data, remote_address):
        return remote_address, data['model_id'], self.federated_learning_wrapper, data

    @normalize_optimized_response(active=True)
    def federated_learning(self, data):
        logging.info("Init federated_learning")
        n_iter = self.config["MAX_ITERATIONS"]
        self.send_requirements_to_data_owner(data)
        logging.info('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        self.encryption_service.set_public_key(data["public_key"])
        models = []
        for i in range(n_iter):
            updates = self.get_updates(data['requirements']['model_type'], data["public_key"])
            updates = self.federated_averaging(updates)
            self.send_global_model(updates)
            models = self.get_trained_models()
            self.model_buyer_connector.send_partial_result(self.federated_averaging(models))

        return self.federated_averaging(models)

    @serialize_encrypted_server_data(schema=json.dumps)
    def federated_learning_wrapper(self, data):
        return self.federated_learning(data)

    def send_global_model(self, weights):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        logging.info("Send global models")
        self.data_owner_connector.send_gradient_to_data_owners(self.data_owners, weights)

    def get_updates(self, requirements, public_key):
        """

        :param requirements:
        :param public_key:
        :return:
        """
        return self.data_owner_connector.get_update_from_data_owners(self.data_owners, requirements, public_key)

    def federated_averaging(self, updates):
        """
        Sum all de partial updates and
        :param updates:
        :return:
        """
        logging.info("Federated averaging")
        return reduce(sum_collection, updates) / len(self.data_owners)

    def get_trained_models(self):
        """obtiene el nombre del modelo a ser entrenado"""
        logging.info("get_trained_models")
        return self.data_owner_connector.get_data_owners_model(self.data_owners)
