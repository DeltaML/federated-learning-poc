import requests
import numpy as np

from commons.decorators.decorators import optimized_collection_response, normalize_optimized_collection


class ClientConnector:

    def __init__(self, client_port):
        self.client_port = client_port

    @optimized_collection_response(optimization=np.asarray, active=True)
    def get_update_from_client(self, client, model_type, public_key):
        """

        :param client:
        :param model_type:
        :param public_key:
        :return:
        """
        url = "http://{}:{}/weights".format(client.host, self.client_port)
        payload = {"type": model_type, "public_key": public_key}
        response = requests.post(url, json=payload)
        return response.json()

    #@normalize_optimized_collection(active=True)
    def send_gradient(self, client, weights):
        """

        :param client:
        :param weights:
        :return:
        """
        url = "http://{}:{}/step".format(client.host, self.client_port)
        payload = {"gradient": weights}
        requests.put(url, json=payload)

    def get_client_model(self, client):
        url = "http://{}:{}/model".format(client.host, self.client_port)
        return requests.get(url).json()
