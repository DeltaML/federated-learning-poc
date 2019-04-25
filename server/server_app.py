import logging
import os
from flask import Flask, request, jsonify

from commons.encryption.encryption_service import EncryptionService
from server.service.server import Server
from server.service.model_service import ModelType

from logging.config import dictConfig

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
    flask_app = Flask(__name__)
    # load the instance config
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    flask_app.config.from_pyfile('config.py')
    return flask_app


def build_encryption_service(config):
    encryption_type = config['ENCRYPTION_TYPE']
    return EncryptionService(encryption_type())


app = create_app()
encryption_service = build_encryption_service(app.config)
server = Server(encryption_service=encryption_service, config=app.config)
logging.info("Server running")

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


@app.route('/clients/register', methods=['POST'])
def register_client():
    # Json contiene url y puerto a donde esta el cliente que se esta logueando
    data = request.get_json()
    data["host"], data["port"] = request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']
    response = server.register_client(data)
    return jsonify(response)


@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify([str(client) for client in server.clients])


@app.route('/predict', methods=['POST'])
def predict():
    input = request.input
    return server.predict(input)


@app.route('/ping', methods=['POST'])
def ping():
    logging.info("Data {}".format(request.get_json()))
    return jsonify("pong")


@app.route('/model', methods=['POST'])
def train_model_async():
    data = request.get_json()
    logging.info("Initializing async model trainig acording to request {}".format(data))
    logging.info("host {} port {}".format(request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']))
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise ValueError(model_type)  # MODIFICAR
    server.process_in_background(request.environ['REMOTE_ADDR'], data)
    return jsonify(200)
