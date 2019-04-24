from commons.encryption.phe_encryption import PheEncryption

ENCRYPTION_TYPE = PheEncryption
ACTIVE_ENCRYPTION = False

config = {
    'n_clients': 5,
    'key_length': 1024,
    'n_iter': 40
}

# TODO: Add in config
CLIENT_PORT = 5000
