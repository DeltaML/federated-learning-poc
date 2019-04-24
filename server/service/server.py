import logging
import requests
from functools import reduce
from threading import Thread

from commons.decorators.decorators import deserialize_encrypted_data, serialize_encrypted_data


class Server:
    def __init__(self, encryption_service, config):
        self.clients = []
        self.encryption_service = encryption_service
        self.public_key = None
        self.config = config

    @staticmethod
    def async_processing(remote_address, call_back_endpoint, func, *args):
        logging.info("process_in_background...")
        remote_host = "http://{}:{}".format(remote_address, 9090)
        call_back_url = "{}/{}".format(remote_host, call_back_endpoint)
        logging.info("call_back_url {}".format(call_back_url))
        result = func(*args)
        requests.post(call_back_url, json=result)

    def process_in_background(self, remote_address, data):
        args = remote_address, data["call_back_endpoint"], self.federated_learning, data['type']
        Thread(target=self.async_processing, args=args).start()

    def federated_learning(self, model_type):
        logging.info("Init federated_learning")
        n_iter = self.config['n_iter']
        logging.info('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        models = []
        for i in range(n_iter):
            updates = self.get_updates(model_type)
            updates = self.federated_averaging(updates)
            self.send_global_model(updates)
            models = self.get_trained_models()
        return models

    @serialize_encrypted_data
    def send_global_model(self, weights):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        for client in self.clients:
            url = "http://{}:{}/step".format(client.ip, self.config.CLIENT_PORT)
            payload = {"gradient": weights}
            requests.put(url, json=payload)

    def register_client(self, client):
        self.clients.append(client)

    @deserialize_encrypted_data
    def _get_update_from_client(self, client, model_type):
        url = "http://{}:{}/weights".format(client.ip, self.config.CLIENT_PORT)
        # TODO: Refactor this
        payload = {"type": model_type}
        response = requests.post(url, json=payload)
        return response.json()

    def get_updates(self, model_type):
        return [self._get_update_from_client(client, model_type) for client in self.clients]

    def federated_averaging(self, updates):
        return reduce(self.encryption_service.sum, updates) / len(self.clients)

    def get_trained_models(self):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        models = []
        for client in self.clients:
            url = "http://{}:{}/model".format(client.ip, self.config.CLIENT_PORT)
            models.append(requests.get(url).json())
        return models
