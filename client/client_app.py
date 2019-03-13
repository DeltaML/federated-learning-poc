import logging
import os
from logging.config import dictConfig

from flask import Flask, request, jsonify, make_response
from client.data.data_loader import get_data
from client.operations_utils.functions import get_encrypted_number, get_deserialized_public_key, get_serialized_gradient
from client.service.client_service import ClientService
from client.service.model_type_service import ModelTypeService

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


def create_client(id, pub_key):
    return ClientService.create_client(app.config['NAME'], X[id], Y[id], pub_key)


# Global variables
app = create_app()
X, Y, X_test, Y_test = get_data(app.config['N_CLIENTS'])
client_id, client_name = app.config['CLIENT_ID'], app.config['NAME']
client = ClientService.create_client(client_name, X[client_id], Y[client_id])


# Single endpoints
@app.route('/create', methods=['POST'])
def client():
    pub_key = request.pub_key
    id = request.id
    client = create_client(id, pub_key)
    return "Client {} was created".format(client.name)


@app.route('/encrypted_gradient', methods=['POST'])
def encrypted_gradient():
    encrypt_aggr = request.encrypt_aggr
    return client.encrypted_gradient(encrypt_aggr)


@app.route('/predict', methods=['POST'])
def predict():
    input = request.input
    return client.predict(input)


# General processing
@app.route('/weights', methods=['POST'])
def process_weights():
    data = request.get_json()
    logging.info("process_weights with {}".format(data))
    # Validate model type
    if not ModelTypeService.validate(data['type']):
        return jsonify(dict(error="Invalid Model Type")), 400

    # Server public key
    pub_key = get_deserialized_public_key(data['pub_key'])
    # encrypt_aggr
    encrypt_aggr = [get_encrypted_number(pub_key, encrypt_value['ciphertext'], encrypt_value['exponent']) for
                    encrypt_value in data['encrypt_aggr']]
    client.pubkey = pub_key
    return jsonify([get_serialized_gradient(value) for value in client.encrypted_gradient(encrypt_aggr)])
