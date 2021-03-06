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


def normalize_optimized_collection_argument(active=False):
    def wrap(f):
        def wrapped_normalize_optimized_collection(*args):
            # TODO: Refactor!!!
            params = args[0], args[1], args[2].tolist() if active else args[2]
            return f(*params)
        return wrapped_normalize_optimized_collection
    return wrap


def normalize_optimized_response(active=False):
    def wrap(f):
        def wrapped_normalize_optimized_response(*args):
            result = f(*args)
            return result.tolist() if active else result
        return wrapped_normalize_optimized_response
    return wrap
