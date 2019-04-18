import logging
import os
from logging.config import dictConfig
from flask import Flask, request, jsonify
from commons.data.data_loader import DataLoader
from client.exceptions.exceptions import InvalidModelException
from client.service.client_service import ClientFactory
from client.service.model_service import ModelType
from client.service.encryption_service import EncryptionService


dictConfig({
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
})


def create_app():
    # create and configure the app
    flask_app = Flask(__name__, instance_relative_config=True)
    # load the instance config
    flask_app.config.from_pyfile('config.py')
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    return flask_app


def register_client(client, config):
    if config['REGISTRATION_ENABLE']:
        client.register(config['N_SEGMENTS'])
        logging.info("Register Number" + str(client.register_number))


# Global variables
app = create_app()
data_loader = DataLoader()
data_loader.load_data(app.config['N_SEGMENTS'])
X_client = None
y_client = None
encryption_type = app.config['ENCRYPTION_TYPE']
encryption_service = EncryptionService(encryption_type())

client = ClientFactory.create_client(app.config, data_loader, encryption_service)
hello = client.hello()
print(hello)
register_client(client, app.config)


@app.errorhandler(Exception)
def handle_error(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }
    return jsonify(response), status_code


@app.route('/weights', methods=['POST'])
def process_weights():
    """
    process weights from server
    :return:
    """
    data = request.get_json()
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise InvalidModelException(model_type)
    # encrypted_model
    return jsonify(client.process(model_type))


@app.route('/step', methods=['PUT'])
def gradient_step():
    """
    Execute step with gradient
    :return:
    """
    data = request.get_json()
    client.step(data["gradient"])
    return jsonify(200)


@app.route('/model', methods=['GET'])
def get_model():
    return jsonify(client.get_model())


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(200)
