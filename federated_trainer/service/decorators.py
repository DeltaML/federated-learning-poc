def deserialize_encrypted_server_data():
    def wrap(f):
        def wrapped_deserialize_encrypted_server_data(*args):
            service = args[0]
            result = f(*args)
            result['update'] = service.encryption_service.get_deserialized_collection(result['update']) if service.active_encryption else result['update']
            return result
        return wrapped_deserialize_encrypted_server_data
    return wrap


def deserialize_encrypted_server_data_2():
    def wrap(f):
        def wrapped_deserialize_encrypted_server_data(*args):
            service = args[0]
            result = f(*args)
            result = service.encryption_service.get_deserialized_collection(result) if service.active_encryption else result
            return result
        return wrapped_deserialize_encrypted_server_data
    return wrap


def serialize_encrypted_server_gradient(schema):
    def wrap(f):
        def wrapped_serialize_encrypted_server_gradient(*args):
            service = args[0]
            data = dict(gradient=service.encryption_service.get_serialized_collection(args[1][1]["gradient"]) if service.active_encryption else args[1][1]["gradient"])
            params = args[0], (args[1][0], data)
            result = f(*params)
            return schema(result)
        return wrapped_serialize_encrypted_server_gradient
    return wrap


def serialize_encrypted_server_data(schema):
    def wrap(f):
        def wrapped_serialize_encrypted_server_data(*args):
            service = args[0]
            result = f(*args)
            response = service.encryption_service.get_serialized_collection(result) if service.active_encryption else result
            return response
        return wrapped_serialize_encrypted_server_data
    return wrap
