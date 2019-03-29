import logging
from commons.model.linear_regression import LinearRegression
from commons.operations_utils.functions import *
import requests
import phe as paillier
from service.model_service import *
from functools import reduce
import numpy as np


# TODO: Add in config
CLIENT_PORT = 5000

class Server:
    def __init__(self, config):
        self.clients = []
        self.keypair = paillier.generate_paillier_keypair(n_length=config['key_length'])
        self.pubkey, self.privkey = self.keypair
        # TODO: add dataset to test
        self.X_test, self.y_test = None, None

    def send_global_model(self, weights):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        for client in self.clients:
            url = "http://{}:{}/step".format(client.ip, CLIENT_PORT)
            payload = {"gradient": weights.tolist()}
            requests.put(url, json=payload)

    def register_client(self, client):
        self.clients.append(client)

    def _get_update_from_client(self, client, model_type):
        url = "http://{}:{}/weights".format(client.ip, CLIENT_PORT)
        #logging.info("CLIENT " + str(client.id) + " URL:" + url)
        # TODO: Refactor this
        payload = {"type": model_type}
        response = requests.post(url, json=payload)
        #logging.info("Response from client " + client.id + ": " + response.text)
        #return response.json()
        return [get_encrypted_number(self.pubkey, encrypt_value['ciphertext'], encrypt_value['exponent']) for encrypt_value in response.json()]

    def get_updates(self, model_type):
        return [self._get_update_from_client(client, model_type) for client in self.clients]

    def federated_averaging(self, updates):
        avg_gradient = reduce(sum_encrypted_vectors, updates)
        #return list(map(lambda x: x / len(self.clients), avg_gradient))
        return self.decrypt_aggregate(avg_gradient, len(self.clients))

    def choose_model(self):
        """
        @Unused
        :return:
        """
        return LinearRegressionModel

    def decrypt_aggregate(self, input_model, n_clients):
        return decrypt_vector(self.privkey, input_model) / n_clients

    def get_trained_models(self):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        models = []
        for client in self.clients:
            url = "http://{}:{}/model".format(client.ip, CLIENT_PORT)
            models.append(requests.get(url).json())
        return models

    def federated_learning(self, model_type, X_test, y_test, config=None):
        n_iter = int(config['n_iter'])
        # Instantiate the server and generate private and public keys
        # NOTE: using smaller keys sizes wouldn't be cryptographically safe
        model = ModelFactory.get_model(model_type)
        # Instantiate the clients.
        # Each client gets the public key at creation and its own local dataset
        # The federated learning with gradient descent
        logging.info('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        for i in range(n_iter):
            #logging.info("Iteration {:d}".format(i))
            updates = self.get_updates(model_type)
            #logging.info("Encrypted gradients " + str(updates))
            updates = self.federated_averaging(updates)
            #logging.info("Averaged gradients" + str(updates))
            self.send_global_model(updates)
            models = self.get_trained_models()
        print('Error (MSE) that each client gets after running the protocol:')
        #logging.info(X_test)
        #logging.info(y_test)
        for i in range(len(self.clients)):
            trained_model =  model(model_type, X_test, y_test)  # updates[i])
            trained_model.set_weights(np.asarray(models[i]))
            y_pred = trained_model.predict(X_test)
            mse = mean_square_error(y_pred, y_test)
            logging.info('Client {:d}:\t{:.2f}'.format(i, mse))
