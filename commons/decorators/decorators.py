def serialize_encrypted_data(encryption_service, schema, active=False):
    def wrap(f):
        def wrapped_serialize_encrypted_data(*args):
            result = f(*args)
            response = encryption_service.get_serialized_collection(result) if active else result
            return schema(response)
        return wrapped_serialize_encrypted_data
    return wrap


def deserialize_encrypted_data(encryption_service, request, active=False):
    def wrap(f):
        def wrapped_deserialize_encrypted_data():
            data = request.get_json()
            result = encryption_service.get_deserialized_collection(data) if active else data
            return f(result)
        return wrapped_deserialize_encrypted_data
    return wrap


def optimized_collection_parameter(optimization, active=False):
    def wrap(f):
        def wrapped_optimized_collection_parameter(*args):
            params = args[0], optimization(args[1]) if active else args[1]
            return f(*params)
        return wrapped_optimized_collection_parameter
    return wrap


def optimized_collection_response(optimization, active=False):
    def wrap(f):
        def wrapped_optimized_collection_response(*args):
            result = f(*args)
            return optimization(result) if active else result
        return wrapped_optimized_collection_response
    return wrap


def normalize_optimized_collection(active=False):
    def wrap(f):
        def wrapped_normalize_optimized_collection(*args):
            params = args.tolist() if active else args
            return f(*params)
        return wrapped_normalize_optimized_collection
    return wrap
