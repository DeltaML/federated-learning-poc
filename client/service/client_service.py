from client.operations_utils.functions import get_deserialized_public_key
from client.service.model_service import ModelFactory


class Client:
    def __init__(self, name, X, y, pubkey=None):
        self.name = name
        self.pubkey = pubkey
        self.X, self.y = X, y
        self.model = None

    def set_public_key(self, pubkey):
        self.pubkey = get_deserialized_public_key(pubkey)

    def process(self, model_type, encrypted_model):
        self.model = self.model if self.model else ModelFactory.get_model(model_type)
        return self.model(self.name, self.X, self.y, self.pubkey).process(encrypted_model)


class ClientFactory:

    @classmethod
    def create_client(cls, name, X, y, pub_key=None):
        return Client(name, X, y, pub_key)
