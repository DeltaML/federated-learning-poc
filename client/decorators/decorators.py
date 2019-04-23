from functools import wraps


def encrypted_response(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        client = args[0]
        result = f(*args, **kwds)
        if client.active_encryption:
            return client.encryption_service.get_serialized_collection(result)
        return result

    return wrapper


def encrypted_request(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        client = args[0]
        result = f(*args, **kwds)
        if client.active_encryption:
            return client.encryption_service.get_deserialized_collection(result)
        return result

    return wrapper


def numpy_optimized(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        client = args[0]
        result = f(*args, **kwds)
        if client.active_encryption:
            return client.encryption_service.get_serialized_collection(result)
        return result

    return wrapper
