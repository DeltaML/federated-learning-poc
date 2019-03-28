from model.linear_regression import LinearRegression
from commons.operations_utils.functions import *
import requests
import phe as paillier
from service.model_service import ModelType


class Server:
    def __init__(self):
        self.clients = []
        self.keypair = paillier.generate_paillier_keypair(n_length=20)
        self.pubkey, self.privkey = self.keypair
        # TODO: add dataset to test
        self.X_test, self.y_test = None, None

    def send_global_model(self, client, weights):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        payload = {"encrypted_model": weights}
        requests.put(client.ip + ":" + client.port + "/step", json=payload)

    def register_client(self, client):
        self.clients.append(client)

    def _get_update_from_client(self, client, model_type):
        url = client.ip + ":" + client.port + "/weights"
        payload = {"type": model_type}
        return requests.post(url, json=payload)

    def get_updates(self, model_type):
        return [self._get_update_from_client(client, model_type) for client in self.clients]

    def update_global_model(self, updates):
        return decrypt_aggregate(sum(updates), len(self.clients))

    def choose_model(self):
        """
        @Unused
        :return:
        """
        return LinearRegressionModel

    def decrypt_aggregate(self, input_model, n_clients):
        return decrypt_vector(self.privkey, input_model) / n_clients


    def federated_learning(self, X_test, y_test, config=None):
        n_iter = 10  # config['n_iter']
        # Instantiate the server and generate private and public keys
        # NOTE: using smaller keys sizes wouldn't be cryptographically safe
        model = ModelFactory.get_model(model_type)
        # Instantiate the clients.
        # Each client gets the public key at creation and its own local dataset
        # The federated learning with gradient descent
        print('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        for i in range(n_iter):
            updates = self.get_updates(model_type, model_type)
            updates = self.update_global_model(updates)
            self.send_global_model(client, updates)
        print('Error (MSE) that each client gets after running the protocol:')
        for i in len(self.clients):
            model = model(model_type, updates[i])
            y_pred = model.predict(X_test)
            mse = mean_square_error(y_pred, y_test)
            print('Client {:s}:\t{:.2f}'.format(i, mse))
