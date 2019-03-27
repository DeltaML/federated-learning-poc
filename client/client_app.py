import logging
import os
from logging.config import dictConfig

from flask import Flask, request, jsonify
from data.data_loader import DataLoader
from exceptions.exceptions import InvalidModelException
from service.client_service import ClientFactory
from service.model_service import ModelType

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
data_loader = DataLoader()
data_loader.load_data(app.config['N_SEGMENTS'])
client_id = app.config['CLIENT_ID']
X_client, y_client = data_loader.get_sub_set(client_id)
client = ClientFactory.create_client(app.config, X_client, y_client)
client.register()


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
    logging.info("process_weights with {}".format(data))
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise InvalidModelException(model_type)
    # encrypted_model
    response = client.process(model_type, data["encrypted_model"])
    return jsonify(response)

@app.route('/step', methods=['PUT'])
def gradient_step():
    data = request.get_json()
    client.step(data["gradient"])
    return jsonify(200) 