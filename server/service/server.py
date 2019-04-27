import logging
import requests
import json
from functools import reduce
from threading import Thread

from commons.decorators.decorators import normalize_optimized_response
from commons.operations_utils.functions import sum_collection
from server.models.client_instance import ClientInstance
from server.service.client_connector import ClientConnector
from server.service.decorators import serialize_encrypted_server_data


class Server:
    def __init__(self, encryption_service, config):
        self.clients = []
        self.encryption_service = encryption_service
        self.config = config
        self.active_encryption = self.config["ACTIVE_ENCRYPTION"]
        self.client_connector = ClientConnector(self.config["CLIENT_PORT"], encryption_service, self.active_encryption)

    def register_client(self, client_data):
        """
        Register new client
        :param client_data:
        :return:
        """

        logging.info("Register client with {}".format(client_data))
        new_client = ClientInstance(client_data)
        self.clients.append(new_client)
        return {'number': len(self.clients)}

    @staticmethod
    def async_server_processing(remote_address, call_back_endpoint, call_back_port, func, *args):
        logging.info("process_in_background...")
        remote_host = "http://{}:{}".format(remote_address, call_back_port)
        call_back_url = "{}/{}".format(remote_host, call_back_endpoint)
        logging.info("call_back_url {}".format(call_back_url))
        result = func(*args)
        requests.post(call_back_url, json=result)

    def process_in_background(self, remote_address, data):
        Thread(target=self.async_server_processing, args=self._build_async_processing_data(data, remote_address)).start()

    def _build_async_processing_data(self, data, remote_address):
        return remote_address, data["call_back_endpoint"], data["call_back_port"], self.federated_learning_wrapper, data['type'], data["public_key"]

    @normalize_optimized_response(active=True)
    def federated_learning(self, model_type, public_key):
        logging.info("Init federated_learning")
        n_iter = self.config["N_ITER"]
        logging.info('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        self.encryption_service.set_public_key(public_key)
        models = []
        for i in range(n_iter):
            updates = self.get_updates(model_type, public_key)
            updates = self.federated_averaging(updates)
            self.send_global_model(updates)
            models = self.get_trained_models()

        return self.federated_averaging(models)

    @serialize_encrypted_server_data(schema=json.dumps)
    def federated_learning_wrapper(self, model_type, public_key):
        return self.federated_learning(model_type, public_key)

    def send_global_model(self, weights):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        logging.info("Send global models")
        self.client_connector.send_gradient_to_clients(self.clients, weights)

    def get_updates(self, model_type, public_key):
        """

        :param model_type:
        :param public_key:
        :return:
        """
        return self.client_connector.get_update_from_clients(self.clients, model_type, public_key)

    def federated_averaging(self, updates):
        """
        Sum all de partial updates and
        :param updates:
        :return:
        """
        logging.info("Federated averaging")
        return reduce(sum_collection, updates) / len(self.clients)

    def get_trained_models(self):
        """obtiene el nombre del modelo a ser entrenado"""
        logging.info("get_trained_models")
        return self.client_connector.get_clients_model(self.clients)
