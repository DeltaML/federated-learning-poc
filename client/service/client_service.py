import uuid
from commons.operations_utils.functions import get_deserialized_public_key
from service.model_service import ModelFactory
from service.server_service import ServerService



class Client:
    def __init__(self, config, X, y):
        """

        :param config:
        :param X:
        :param y:
        """
        self.client_id = str(uuid.uuid1())
        self.client_name = "CLIENT {}".format(self.client_id)
        self.config = config
        self.X, self.y = X, y
        self.model = None
        self.pubkey = None
        self.training_model = None

    def process(self, model_type, encrypted_model):
        """
        Process to run encrypted model
        :param model_type:
        :param encrypted_model:
        :return:
        """
        self.model = self.model if self.model else ModelFactory.get_model(model_type)
        self.training_model = self.model(self.client_name, self.X, self.y, self.pubkey)
        return self.training_model.process(encrypted_model)

    def register(self):
        """
        Register client into federated server
        :return:
        """
        response = ServerService(self.config).register(self._get_register_data())
        self.pubkey = get_deserialized_public_key(response['pub_key'])

    def _get_register_data(self):
        return {'id': self.client_id}

    def step(self, encrypted_model):
        self.training_model.gradient_step(encrypted_model)


class ClientFactory:
    @classmethod
    def create_client(cls, name, X, y):
        """
        Create new client
        :param name:
        :param X:
        :param y:
        :return:
        """
        return Client(name, X, y)
