config = {
    'FEDERATED_TRAINER_HOST': "http://localhost:8080",
    'key_length': 1024,
    'port': 9090,
    'active_encryption': False,
    'DATASETS_DIR': "./dataset/"
}

logging_config = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}