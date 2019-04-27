def serialize_encrypted_data(encryption_service, schema, active=False):
    def wrap(f):
        def wrapped_serialize_encrypted_data(*args):
            result = f(*args)
            response = encryption_service.get_serialized_collection(result, encrypted=active) if active else result
            return schema(response)
        return wrapped_serialize_encrypted_data
    return wrap


def deserialize_encrypted_data(encryption_service, request, active=False):
    def wrap(f):
        def wrapped_deserialize_encrypted_data():
            data = request.get_json()["gradient"]
            result = encryption_service.get_deserialized_collection(data) if active else data
            return f(result)
        return wrapped_deserialize_encrypted_data
    return wrap
