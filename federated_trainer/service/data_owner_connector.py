import requests
import numpy as np
import json
from commons.decorators.decorators import optimized_collection_response, normalize_optimized_collection
from federated_trainer.service.decorators import deserialize_encrypted_server_data, serialize_encrypted_server_gradient
from commons.utils.async_thread_pool_executor import AsyncThreadPoolExecutor


class DataOwnerConnector:

    def __init__(self, data_owner_port, encryption_service, active_encryption):
        self.data_owner_port = data_owner_port
        self.async_thread_pool = AsyncThreadPoolExecutor()
        self.encryption_service = encryption_service
        self.active_encryption = active_encryption

    def send_gradient_to_data_owners(self, data_owners, weights):
        args = [self._build_data(data_owner, weights) for data_owner in data_owners]
        self.async_thread_pool.run(executable=self._send_gradient, args=args)

    @optimized_collection_response(optimization=np.asarray, active=True)
    def get_update_from_data_owners(self, data_owners, model_type, public_key):
        args = [(data_owner, model_type, public_key) for data_owner in data_owners]
        return self.async_thread_pool.run(executable=self._get_update_from_data_owner, args=args)

    @optimized_collection_response(optimization=np.asarray, active=True)
    def get_data_owners_model(self, data_owners):
        args = ["http://{}:{}/model".format(data_owner.host, self.data_owner_port) for data_owner in data_owners]
        results = self.async_thread_pool.run(executable=self._get_data_owner_model, args=args)
        return [result for result in results]

    @deserialize_encrypted_server_data()
    def _get_update_from_data_owner(self, data):
        """

        :param data:
        :return:
        """
        data_owner, model_type, public_key = data
        url = "http://{}:{}/weights".format(data_owner.host, self.data_owner_port)
        payload = {"type": model_type, "public_key": public_key}
        response = requests.post(url, json=payload)
        return response.json()

    @serialize_encrypted_server_gradient(schema=json.dumps)
    def _send_gradient(self, data):
        """
        Replace with parallel
        :param data:
        :return:
        """
        url, payload = data
        requests.put(url, json=payload)

    @deserialize_encrypted_server_data()
    def _get_data_owner_model(self, url):
        return requests.get(url).json()

    # ---
    @normalize_optimized_collection(active=True)
    def _build_data(self, data_owner, weights):
        return "http://{}:{}/step".format(data_owner.host, self.data_owner_port), {"gradient": weights}
