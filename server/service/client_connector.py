import requests
import numpy as np
import json
from commons.decorators.decorators import optimized_collection_response, normalize_optimized_collection
from server.service.decorators import deserialize_encrypted_server_data, serialize_encrypted_server_gradient
from commons.utils.async_thread_pool_executor import AsyncThreadPoolExecutor


class ClientConnector:

    def __init__(self, client_port, encryption_service, active_encryption):
        self.client_port = client_port
        self.async_thread_pool = AsyncThreadPoolExecutor()
        self.encryption_service = encryption_service
        self.active_encryption = active_encryption

    @deserialize_encrypted_server_data()
    def get_update_from_client(self, data):
        """

        :param data:
        :return:
        """
        client, model_type, public_key = data
        url = "http://{}:{}/weights".format(client.host, self.client_port)
        payload = {"type": model_type, "public_key": public_key}
        response = requests.post(url, json=payload)
        return response.json()

    @serialize_encrypted_server_gradient(schema=json.dumps)
    def send_gradient(self, data):
        """
        Replace with parallel
        :param client:
        :return:
        """
        url, payload = data
        requests.put(url, json=payload)

    @deserialize_encrypted_server_data()
    def get_client_model(self, url):
        return requests.get(url).json()

    @optimized_collection_response(optimization=np.asarray, active=True)
    def get_clients_model(self, clients):
        args = ["http://{}:{}/model".format(client.host, self.client_port) for client in clients]
        results = self.async_thread_pool.run(executable=self.get_client_model, args=args)
        return [result for result in results]

    # ---
    @normalize_optimized_collection(active=True)
    def _build_data(self, client, weights):
        return "http://{}:{}/step".format(client.host, self.client_port), {"gradient": weights}

    def send_gradient_to_clients(self, clients, weights):
        args = [self._build_data(client, weights) for client in clients]
        self.async_thread_pool.run(executable=self.send_gradient, args=args)

    @optimized_collection_response(optimization=np.asarray, active=True)
    def get_update_from_clients(self, clients, model_type, public_key):
        args = [(client, model_type, public_key) for client in clients]
        return self.async_thread_pool.run(executable=self.get_update_from_client, args=args)

