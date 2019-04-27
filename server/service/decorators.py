def deserialize_encrypted_server_data():
    def wrap(f):
        def wrapped_deserialize_encrypted_server_data(*args):
            client = args[0]
            result = f(*args)
            return client.encryption_service.get_deserialized_collection(result) if client.active_encryption else result
        return wrapped_deserialize_encrypted_server_data
    return wrap


def serialize_encrypted_server_data(schema):
    def wrap(f):
        def wrapped_serialize_encrypted_server_data(*args):
            client = args[0]
            data = dict(gradient=client.encryption_service.get_serialized_collection(args[1][1]["gradient"]) if client.active_encryption else args[1][1]["gradient"])
            params = args[0], (args[1][0], data)
            result = f(*params)
            return schema(result)
        return wrapped_serialize_encrypted_server_data
    return wrap

