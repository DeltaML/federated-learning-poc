import numpy as np
import phe as paillier


def mean_square_error(y_pred, y):
    """ 1/m * \sum_{i=1..m} (y_pred_i - y_i)^2 """
    return np.mean((y - y_pred) ** 2)


def encrypt_vector(public_key, x):
    return [public_key.encrypt(i) for i in x]


def decrypt_vector(private_key, x):
    return np.array([private_key.decrypt(i) for i in x])


def sum_encrypted_vectors(x, y):
    if len(x) != len(y):
        raise ValueError('Encrypted vectors must have the same size')
    return [x[i] + y[i] for i in range(len(x))]


def get_deserialized_public_key(pk):
    return paillier.PaillierPublicKey(n=int(pk))


def get_encrypted_number(pub_key, ciphertext, exponent):
    """
    :param pub_key:
    :param ciphertext:
    :param exponent:
    :return:
    """
    return paillier.EncryptedNumber(pub_key, int(ciphertext), int(exponent))


def get_serialized_encrypted_value(value):
    return dict(ciphertext=str(value.ciphertext()), exponent=value.exponent)
