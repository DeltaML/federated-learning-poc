import phe as paillier
import numpy as np
from fractions import Fraction
init_values = [['7.44012909e-02', '-4.46416365e-02', '1.14508998e-01', '2.87580964e-02',
                '2.45741445e-02', '2.49905934e-02', '1.91869970e-02', '-2.59226200e-03',
                '-6.09254186e-04', '-5.21980442e-03', '1.00000000e+00'],
               ['1.62806757e-02', '5.06801187e-02', '-4.60850009e-02', '1.15437429e-02',
                '-3.32158756e-02', '-1.60318551e-02', '-1.02661054e-02', '-2.59226200e-03',
                '-4.39854026e-02', '-4.24987666e-02', '1.00000000e+00'],
               ['1.62806757e-02', '-4.46416365e-02', '2.07393477e-02', '2.18723550e-02',
                '-1.39525355e-02', '-1.32135190e-02', '-6.58446761e-03', '-2.59226200e-03',
                '1.33159679e-02', '4.03433716e-02', '1.00000000e+00'],
               ['5.98711371e-02', '5.06801187e-02', '1.64280994e-02', '2.87580964e-02',
                '-4.14715927e-02', '-2.91840905e-02', '-2.86742944e-02', '-2.59226200e-03',
                '-2.39668149e-03', '-2.17882321e-02', '1.00000000e+00'],
               ['4.53409833e-02', '5.06801187e-02', '6.06183944e-02', '3.10533436e-02',
                '2.87020031e-02', '-4.73467013e-02', '-5.44457591e-02', '7.12099798e-02',
                '1.33598980e-01', '1.35611831e-01', '1.00000000e+00']]


def divide_values_by_scalar(values, scalar):
    return values / scalar


def encrypt_vector(public_key, values):
    return np.vectorize(lambda x: public_key.encrypt(x))(values)


def decrypt_vector(private_key, values):
    return [private_key.decrypt(x) for x in values]


if __name__ == "__main__":
    """
    float_values = [float(v) for v_array in init_values for v in v_array]

    pubkey, privkey = paillier.generate_paillier_keypair()
    encrypted_values = encrypt_vector(pubkey, float_values)
    divided_values = encrypted_values
    for i in range(1, 100):
        divided_values = divide_values_by_scalar(divided_values, 1.0)
    dec_value = decrypt_vector(privkey, divided_values)
    print( dec_value == float_values)

    public_key, privkey = paillier.generate_paillier_keypair()
    one_int = 1
    one_float = float(1.0)
    print(one_int)
    print(one_float)
    encoded_int = paillier.EncodedNumber.encode(public_key, one_int, precision=1e2)
    encoded_float = paillier.EncodedNumber.encode(public_key, one_float, precision=1e2)
    encrypted_int = public_key.encrypt(one_int, precision=1e2)
    encrypted_float = public_key.encrypt(one_float, precision=1e2)
    for i in range(1, 100):
        print(encrypted_int.exponent)
        print(encrypted_float.exponent)
        encrypted_int = encrypted_int / 1.0
        encrypted_float = encrypted_float / 1.0
    print(privkey.decrypt(encrypted_int))
    print(privkey.decrypt(encrypted_float))
    """
