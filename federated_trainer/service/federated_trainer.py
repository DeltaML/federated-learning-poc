import logging
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
        self.data_owners = {}
        self.encryption_service = encryption_service
        self.config = config
        self.active_encryption = self.config["ACTIVE_ENCRYPTION"]
        self.data_owner_connector = DataOwnerConnector(self.config["DATA_OWNER_PORT"], encryption_service, self.active_encryption)
        self.model_buyer_connector = ModelBuyerConnector(self.config["MODEL_BUYER_PORT"])
        self.linked_data_owners = {}

    def register_data_owner(self, data_owner_data):
        """
        Register new data_owner
        :param data_owner_data:
        :return:
        """

        logging.info("Register data owner with {}".format(data_owner_data))
        new_data_owner = DataOwnerInstance(data_owner_data)
        self.data_owners[new_data_owner.id] = new_data_owner
        return {'number': len(self.data_owners)}

    def send_requirements_to_data_owner(self, data):
        return self.data_owner_connector.send_requirements_to_data_owners(list(self.data_owners.values()), data)

    def async_server_processing(self, remote_address, model_id, func, *args):
        logging.info("process_in_background...")
        self.model_buyer_connector.set_remote_buyer_data(remote_address, model_id)
        result = func(*args)
        self.model_buyer_connector.send_result(result)

    def process(self, remote_address, data):
        Thread(target=self.async_server_processing, args=self._build_async_processing_data(data, remote_address)).start()

    def _build_async_processing_data(self, data, remote_address):
        return remote_address, data['model_id'], self.federated_learning_wrapper, data

    def _link_data_owners_to_model_training(self, data):
        owners_with_data = self.send_requirements_to_data_owner(data)
        for data_owner_link in owners_with_data:
            if (data['model_id'] in data_owner_link) and (data_owner_link[data['model_id']][1]):
                data_owner_key = data_owner_link[data['model_id']][0]
                if data['model_id'] not in self.linked_data_owners:
                    self.linked_data_owners[data['model_id']] = []
                self.linked_data_owners[data['model_id']].append(self.data_owners[data_owner_key])


    @normalize_optimized_response(active=True)
    def federated_learning(self, data):
        logging.info("Init federated_learning")
        n_iter = self.config["MAX_ITERATIONS"]
        model_id = data['model_id']
        self._link_data_owners_to_model_training(data)
        logging.info('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        self.encryption_service.set_public_key(data["public_key"])
        models = []
        for i in range(n_iter):
            updates = self.get_updates(data['requirements']['model_type'], data["public_key"], model_id)
            updates = self.federated_averaging(updates, model_id)
            self.send_global_model(updates, model_id)
            models = self.get_trained_models(model_id)
            self.model_buyer_connector.send_partial_result(self.federated_averaging(models, model_id))

        return self.federated_averaging(models, model_id)

    @serialize_encrypted_server_data(schema=json.dumps)
    def federated_learning_wrapper(self, data):
        return self.federated_learning(data)

    def send_global_model(self, weights, model_id):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        logging.info("Send global models")
        self.data_owner_connector.send_gradient_to_data_owners(self.linked_data_owners[model_id], weights)

    def get_updates(self, requirements, public_key, model_id):
        """
        :param requirements:
        :param public_key:
        :param model_id
        :return:
        """
        return self.data_owner_connector.get_update_from_data_owners(self.linked_data_owners[model_id], requirements, public_key)

    def federated_averaging(self, updates, model_id):
        """
        Sum all de partial updates and
        :param updates:
        :return:
        """
        logging.info("Federated averaging")
        return reduce(sum_collection, updates) / len(self.linked_data_owners[model_id])

    def get_trained_models(self, model_id):
        """obtiene el nombre del modelo a ser entrenado"""
        logging.info("get_trained_models")
        return self.data_owner_connector.get_data_owners_model(self.linked_data_owners[model_id])
