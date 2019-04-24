class HomomorphicEncryption(object):

    def __init__(self, public_key=None, private_key=None):
        self.public_key = public_key
        self.private_key = private_key

    def encrypt_collection(self, public_key, collection):
        pass

    def decrypt_collection(self, private_key, collection):
        pass

    def get_deserialized_public_key(self, public_key):
        pass

    def get_encrypted_number(self, pub_key, value):
        pass

    def get_serialized_encrypted_number(self, value):
        pass
