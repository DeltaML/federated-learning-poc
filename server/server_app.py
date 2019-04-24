import logging
import os
import requests
from flask import Flask, request, jsonify

from client.service.encryption_service import EncryptionService
from commons.data.data_loader import DataLoader
from server.service.server import Server
from server.ClientInstance import ClientInstance
from server.service.model_service import ModelType


def create_app():
    # create and configure the app
    flask_app = Flask(__name__, instance_relative_config=True)
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    return flask_app


app = create_app()
encryption_type = app.config['ENCRYPTION_TYPE']
encryption_service = EncryptionService(encryption_type())

server = Server(encryption_service=encryption_service, config=app.config)


# Single endpoints
@app.route('/clients/register', methods=['POST'])
def register_client():
    # Json contiene url y puerto a donde esta el cliente que se esta logueando
    data = request.get_json()
    data["ip"], data["port"] = request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']
    logging.info("Register client with data {}".format(data))
    new_client = ClientInstance(data, server.public_key)
    server.register_client(new_client)
    response = {'pub_key': new_client.pub_key, 'number': len(server.clients)}
    return jsonify(response)


@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify([str(client) for client in server.clients])


@app.route('/predict', methods=['POST'])
def predict():
    input = request.input
    return server.predict(input)


# General processing
@app.route('/model', methods=['POST'])
def train_model():
    data = request.get_json()
    logging.info("Initializing model trainig acording to request {}".format(data))
    # Validate model type
    model_type = data['type']
    data_loader = DataLoader()
    data_loader.load_data(5)
    if not ModelType.validate(model_type):
        raise ValueError(model_type)  # MODIFICAR
    response = server.federated_learning(model_type, data_loader.X_test, data_loader.y_test)
    return jsonify(response)


@app.route('/ping', methods=['POST'])
def ping():
    logging.info("Data {}".format(request.get_json()))
    return jsonify("pong")


@app.route('/async', methods=['POST'])
def train_model_async():
    data = request.get_json()
    logging.info("Initializing async model trainig acording to request {}".format(data))
    logging.info("host {} port {}".format(request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']))
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise ValueError(model_type)  # MODIFICAR
    server.pub_key = data["public_key"]
    server.process_in_background(request.environ['REMOTE_ADDR'], data)
    return jsonify(200)
