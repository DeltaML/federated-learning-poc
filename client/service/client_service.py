import uuid

from client.service.model_service import ModelFactory
from client.service.server_service import ServerService
from commons.decorators.decorators import deserialize_encrypted_data, serialize_encrypted_data


class Client:

    def __init__(self, config, data_loader, encryption_service):
        """
        :param config:
        :param data_loader:
        :param encryption_service:
        """

        self.client_id = str(uuid.uuid1())
        self.client_name = "CLIENT {}".format(self.client_id)
        self.config = config
        self.data_loader = data_loader
        self.encryption_service = encryption_service
        self.register_number = None
        self.model = None

    def process(self, model_type):
        """
        Process to run encrypted model
        :param model_type:
        :return:
        """
        X, y = self.data_loader.get_sub_set(self.get_client_register_number())
        model = self.model if self.model else ModelFactory.get_model(model_type)(X, y)
        return model.compute_gradient()

    def register(self):
        """
        Register client into federated server
        :return:
        """
        response = ServerService(self.config).register(self._get_register_data())
        self.register_number = int(response['number']) - 1
        return response

    def _get_register_data(self):
        return {'id': self.client_id}

    def step(self, encrypted_model):
        self.model.gradient_step(encrypted_model, self.config['eta'])

    def get_client_register_number(self):
        return self.register_number

    def get_model(self):
        return self.model.weights


class ClientFactory:
    @classmethod
    def create_client(cls, name, data_loader, encryption_service):
        """
        :param name:
        :param data_loader:
        :param encryption_service:
        :return:
        """
        return Client(name, data_loader, encryption_service)
