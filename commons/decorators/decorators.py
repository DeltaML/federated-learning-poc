def serialize_encrypted_data(encryption_service, schema, active=False):
    def wrap(f):
        def wrapped_f(*args):
            result = f(*args)
            response = encryption_service.get_serialized_collection(result) if active else result
            return schema(response)
        return wrapped_f
    return wrap


def deserialize_encrypted_data(encryption_service, request, active=False):
    def wrap(f):
        def wrapped_f2():
            data = request.get_json()
            result = encryption_service.get_deserialized_collection(data) if active else data
            return f(*result)
        return wrapped_f2
    return wrap


def optimized(engine, active):
    def wrap(f):
        def wrapped_f3(*args):
            result = f(*args)
            return result
        return wrapped_f3
    return wrap
