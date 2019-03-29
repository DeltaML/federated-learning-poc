import uuid
from commons.operations_utils.functions import get_deserialized_public_key
from service.model_service import ModelFactory
from service.server_service import ServerService
from random import randint


config = {
    'eta': 1.5
}


class Client:

    model = None

    def __init__(self, config, data_loader):
        """
        :param config:
        :param X:
        :param y:
        """
        self.client_id = str(uuid.uuid1())
        self.client_name = "CLIENT {}".format(self.client_id)
        self.config = config
        self.X = None
        self.y = None
        self.pubkey = None
        self.register_number = None
        self.data_loader = data_loader

    def _create_model(self, model_type):
        new_model = ModelFactory.get_model(model_type)
        return new_model(self.client_name, self.X, self.y, self.pubkey)

    def process(self, model_type):
        """
        Process to run encrypted model
        :param model_type:
        :param encrypted_model:
        :return:
        """
        self.model = self.model if self.model else self._create_model(model_type)
        return self.model.process()

    def register(self, segments):
        """
        Register client into federated server
        :return:
        """
        response = ServerService(self.config).register(self._get_register_data())
        self.pubkey = get_deserialized_public_key(response['pub_key'])
        self.register_number = int(response['number']) - 1
        self.X, self.y = self.data_loader.get_sub_set(self.get_client_segment(segments))

    def _get_register_data(self):
        return {'id': self.client_id}

    def step(self, encrypted_model):
        self.model.gradient_step(encrypted_model, config['eta'])


    def get_client_segment(self, n_segments):
        return self.register_number


class ClientFactory:
    @classmethod
    def create_client(cls, name, data_loader):
        """
        Create new client
        :param name:
        :param X:
        :param y:
        :return:
        """
        return Client(name, data_loader)
