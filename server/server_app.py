import logging
import sys, os
from logging.config import dictConfig
from flask import Flask, request, jsonify
from operations_utils.functions import get_encrypted_number, get_deserialized_public_key, get_serialized_gradient
from requests import post
from Server import Server


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
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    return flask_app

CLIENTS = []
server = Server()
app = create_app()

# Single endpoints
@app.route('/clients/register', methods=['POST'])
def register_client():
    # Json contiene url y puerto a donde esta el cliente que se esta logueando
    data = request.get_json()
    new_client = ClientInstance(data)
    server.register_clients(new_client)
    return jsonify(new_client)


@app.route('/clients', methods=['GET'])
def get_clients():
    return server.clients


@app.route('/predict', methods=['POST'])
def predict():
    input = request.input
    return server.predict(input)


# General processing
@app.route('/model', methods=['POST'])
def train_model():
    data = request.get_json()
    logging.info("process_weights with {}".format(data))
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise InvalidModelException(model_type)
    #server.federated_learning()
    response = "hola"
    return jsonify(response)
