import requests
import numpy as np

from commons.decorators.decorators import optimized_collection_response, normalize_optimized_collection
from commons.utils.async_thread_pool_executor import AsyncThreadPoolExecutor


class ClientConnector:

    def __init__(self, client_port):
        self.client_port = client_port
        self.async_thread_pool = AsyncThreadPoolExecutor()

    def get_update_from_client(self, data):
        """

        :param client:
        :param model_type:
        :param public_key:
        :return:
        """
        client, model_type, public_key = data
        url = "http://{}:{}/weights".format(client.host, self.client_port)
        payload = {"type": model_type, "public_key": public_key}
        response = requests.post(url, json=payload)
        return response.json()

    def send_gradient(self, data):
        """
        Replace with parallel
        :param client:
        :return:
        """
        url, payload = data
        requests.put(url, json=payload)

    @optimized_collection_response(optimization=np.asarray, active=True)
    def get_clients_model(self, clients):
        args = ["http://{}:{}/model".format(client.host, self.client_port) for client in clients]
        results = self.async_thread_pool.run(executable=requests.get, args=args)
        return [result.json() for result in results]

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

