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

    def _create_model(self, model_type):
        model = ModelFactory.get_model(model_type)
        return model(self.client_name, self.X, self.y, self.pubkey)

    def process(self, model_type):
        """
        Process to run encrypted model
        :param model_type:
        :param encrypted_model:
        :return:
        """
        self.model = self.model if self.model else self._create_model(model_type)
        return self.model.process()

    def register(self):
        """
        Register client into federated server
        :return:
        """
        response = ServerService(self.config).register(self._get_register_data())
        self.pubkey = get_deserialized_public_key(response['pub_key'])

    def _get_register_data(self):
        return {'id': self.client_id}

    def make_step(self, encrypted_model):
        TRAINED_MODELS[self.client_id].gradient_step(encrypted_model)


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
