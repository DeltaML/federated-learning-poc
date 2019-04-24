import phe as paillier

from commons.encryption.homomorphic_encryption import HomomorphicEncryption


class PheEncryption(HomomorphicEncryption):

    def encrypt_collection(self, public_key, collection):
        return [public_key.encrypt(i) for i in collection]

    def decrypt_collection(self, private_key, collection):
        return [private_key.decrypt(i) for i in collection]

    def get_deserialized_public_key(self, public_key):
        return paillier.PaillierPublicKey(n=int(public_key))

    def get_encrypted_number(self, pub_key, value):
        ciphertext, exponent = value
        return paillier.EncryptedNumber(pub_key, int(ciphertext), int(exponent))

    def get_serialized_encrypted_number(self, value):
        return dict(ciphertext=str(value.ciphertext()), exponent=value.exponent)
