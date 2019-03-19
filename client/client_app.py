import logging
import os
from logging.config import dictConfig

from flask import Flask, request, jsonify
from client.data.data_loader import get_data
from client.exceptions.exceptions import InvalidModelException
from client.service.client_service import ClientFactory
from client.service.model_service import ModelType


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


# Global variables
app = create_app()
X, Y, X_test, Y_test = get_data(app.config['N_CLIENTS'])
client_id, client_name = app.config['CLIENT_ID'], app.config['NAME']
client = ClientFactory.create_client(client_name, X[client_id], Y[client_id])


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
    data = request.get_json()
    logging.info("process_weights with {}".format(data))
    # Validate model type
    model_type = data['type']

    if not ModelType.validate(model_type):
        raise InvalidModelException(model_type)

    # Server public key
    client.set_public_key(data['pub_key'])
    # encrypted_model
    response = client.process(model_type, data["encrypted_model"])
    return jsonify(response)
