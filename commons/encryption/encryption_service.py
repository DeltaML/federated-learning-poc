from commons.encryption.config import ENCRYPTION_TYPE


class EncryptionService:

    def __init__(self, homomorphic_encryption=ENCRYPTION_TYPE):
        """

        :param homomorphic_encryption:
        """
        self.homomorphic_encryption = homomorphic_encryption
        self.public_key = None

    def set_public_key(self, public_key):
        """

        :param public_key:
        :return:
        """
        self.public_key = self.homomorphic_encryption.get_deserialized_public_key(public_key)

    def encrypt_collection(self, collection):
        """

        :param collection:
        :return:
        """
        return self.homomorphic_encryption.encrypt_collection(self.public_key, collection)

    def decrypt_collection(self, private_key, collection):
        """

        :param collection:
        :return:
        """
        return self.homomorphic_encryption.decrypt_collection(private_key, collection)


    def decrypt_and_deserizalize_collection(self, private_key, collection):
        return [self.homomorphic_encryption.decrypt_value(private_key, n) for n in self.get_deserialized_collection(collection)]

    def get_serialized_encrypted_collection(self, collection):
        """

        :param collection:
        :return:
        """

        return [self.get_serialized_encrypted_value(value) for value in self.encrypt_collection(collection)]

    def get_serialized_collection(self, collection):
        """

        :param collection:
        :return:
        """
        return [self.get_serialized_encrypted_value(value) for value in collection]

    def get_deserialized_collection(self, collection):
        """

        :param collection:
        :return:
        """
        return [self.get_deserialized_encrypted_value(value) for value in collection]

    def get_serialized_encrypted_value(self, value):
        """

        :param value:
        :return:
        """
        return self.homomorphic_encryption.get_serialized_encrypted_number(value)

    def get_deserialized_encrypted_value(self, value):
        """

        :param value:
        :return:
        """
        return self.homomorphic_encryption.get_encrypted_number(self.public_key, value)

    def generate_key_pair(self, key_length):
        """

        :param key_length:
        :return:
        """
        return self.homomorphic_encryption.generate_key_pair(key_length)
