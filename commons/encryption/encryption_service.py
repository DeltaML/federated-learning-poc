from commons.encryption.config import ENCRYPTION_TYPE


class EncryptionService:

    def __init__(self, homomorphic_encryption=ENCRYPTION_TYPE):
        """

        :param homomorphic_encryption:
        """
        self.homomorphic_encryption = homomorphic_encryption()
        self.public_key, self.private_key = None, None

    def generate_key_pair(self, key_length):
        """

        :param key_length:
        :return:
        """
        self.public_key, self.private_key = self.homomorphic_encryption.generate_key_pair(key_length=key_length)
        return self.public_key, self.private_key

    def get_public_key(self):
        """

        :return:
        """
        return self.public_key.n

    def get_private_key(self):
        """

        :return:
        """
        return self.private_key

    def set_public_key(self, public_key):
        """

        :param public_key:
        :return:
        """
        self.public_key = self.homomorphic_encryption.get_deserialized_public_key(public_key)

    def encrypt_collection(self, collection, public_key=None):
        """

        :param collection:
        :param public_key:
        :return:
        """
        pk = public_key if public_key else self.public_key
        return self.homomorphic_encryption.encrypt_collection(pk, collection)

    def decrypt_collection(self, collection, private_key=None):
        """

        :param collection:
        :param private_key:
        :return:
        """
        pk = private_key if private_key else self.private_key
        return self.homomorphic_encryption.decrypt_collection(pk, collection)

    def decrypt_and_deserizalize_collection(self, private_key, collection):
        return [self.homomorphic_encryption.decrypt_value(private_key, n) for n in self.get_deserialized_collection(collection)]

    def get_serialized_encrypted_collection(self, collection):
        """

        :param collection:
        :return:
        """

        return [self.__get_serialized_encrypted_value(value) for value in self.encrypt_collection(collection)]

    def get_serialized_collection(self, collection):
        """

        :param collection:
        :return:
        """
        return [self.__get_serialized_encrypted_value(value) for value in collection]

    def get_deserialized_collection(self, collection):
        """

        :param collection:
        :return:
        """
        return [self.__get_deserialized_encrypted_value(value) for value in collection]

    def __get_serialized_encrypted_value(self, value):
        """

        :param value:
        :return:
        """
        return self.homomorphic_encryption.get_serialized_encrypted_number(value)

    def __get_deserialized_encrypted_value(self, value):
        """

        :param value:
        :return:
        """
        return self.homomorphic_encryption.get_encrypted_number(self.public_key, value)
