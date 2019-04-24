from functools import wraps
import numpy as np


def serialize_encrypted_data(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        service = args[0]
        result = f(*args, **kwds)
        if service.active_encryption:
            return service.encryption_service.get_serialized_collection(result)
        return result

    return wrapper


def deserialize_encrypted_data(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        service = args[0]
        result = f(*args, **kwds)
        if service.active_encryption:
            return service.encryption_service.get_deserialized_collection(result)
        return result

    return wrapper


def numpy_optimized(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        service = args[0]
        result = f(*args, **kwds)
        if service.active_optimization:
            return np.asarray(result)
        return result

    return wrapper
