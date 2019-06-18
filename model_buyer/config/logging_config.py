import os

DEV_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s - %(message)s'
        },
        'with_filename': {
            'format': '%(asctime)s (%(hostname)s-%(pathname)s:%(lineno)d '
                      '%(levelname)s [%(current_execution)s] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'my_module': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': 'no'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
        'propagate': 'no'
    }
}


PROD_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s (%(hostname)s) %(levelname)s [%(current_execution)s] - %(message)s'
        },
        'with_filename': {
            'format': '%(asctime)s (%(hostname)s-%(pathname)s:%(lineno)d '
                      '%(levelname)s [%(current_execution)s] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'maxBytes': (1024**2)*5,  # 5MB
            'backupCount': 5,  # Stores from app.log to app.log.5
            'formatter': 'simple',
            'filename': os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) + '/logs/app.log'
        }
    },
    'loggers': {
        'my_module': {
            'level': 'INFO',
            'handlers': ['console', 'file_handler'],
            'propagate': 'no'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file_handler'],
        'propagate': 'no'
    }
}