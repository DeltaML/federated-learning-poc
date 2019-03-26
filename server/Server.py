from model.linear_regression import LinearRegression
from operations_utils.functions import *
import requests
import phe as paillier

class Server:

    def __init__(self, key_length=20):
        self.clients = []
        self.keypair = paillier.generate_paillier_keypair(n_length=key_length)
        self.pubkey, self.privkey = self.keypair

    def sendGlobalModel(self, modelName):
        """Encripta y envia el nombre del modelo a ser entrenado"""
        return requests.post()

    def sendModelTypeToClient(client, model_type):
        requests.post(paillier.encrypt(model_type))

    def register_client(self, client):
        self.clients.append(client)

    def _getUpdateFromClient(client):
        return requests.get(client.ip + ":" + client.port + "/weights")

    def getUpdates(self):
        return [_getUpdateFromClient(client) for client in self.clients]

    def updateGlobalModel(self, model, updates):
        return server.decrypt_aggregate(sum(updates), len(self.clients))

    def chooseModel(self):
        return LinearRegressionModel

    def decrypt_aggregate(self, input_model, n_clients):
        return decrypt_vector(self.privkey, input_model) / n_clients

    def federated_learning(X_test, y_test, config):
        n_iter = config['n_iter']
        # Instantiate the server and generate private and public keys
        # NOTE: using smaller keys sizes wouldn't be cryptographically safe
        server = Server(key_length=config['key_length'])
        model = ModelFactory.get_model(model_type)
        n_clients = len(self.clients)

        # Instantiate the clients.
        # Each client gets the public key at creation and its own local dataset
        for client in self.clients:
            if not sendModelTypeToClient(client, model_type):
                raise RuntimeError

        # The federated learning with gradient descent
        print('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        for i in range(n_iter):
            updates = getUpdates()
            updates = updateGlobalModel(model, updates)
            sendGlobalModel(client, updates)