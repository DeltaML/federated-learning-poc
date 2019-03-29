import logging
import os
import threading
import requests
import asyncio
import concurrent.futures
from logging.config import dictConfig
from flask import Flask, request, jsonify
from commons.data.data_loader import DataLoader
from Server import Server
from ClientInstance import ClientInstance
from service.model_service import ModelType
from threading import Thread


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

config = {
    'n_clients': 5,
    'key_length': 1024,
    'n_iter': 40
}


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
server = Server(config)
app = create_app()


# Single endpoints
@app.route('/clients/register', methods=['POST'])
def register_client():
    # Json contiene url y puerto a donde esta el cliente que se esta logueando
    data = request.get_json()
    data["ip"], data["port"] = request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']
    logging.info("Register client with data {}".format(data))
    new_client = ClientInstance(data, server.pubkey.n)
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
    response = server.federated_learning(model_type, data_loader.X_test, data_loader.y_test, config)
    return jsonify(response)


@app.route('/ping', methods=['POST'])
def ping():
    logging.info("Data {}".format(request.get_json()))
    return jsonify("pong")


def async_processing(request_env, call_back_endpoint, func, *args):
    logging.info("process_in_background...")
    remote_host = "http://{}:{}".format(request_env['REMOTE_ADDR'], 9090)
    call_back_url = "{}/{}".format(remote_host, call_back_endpoint)
    logging.info("call_back_url {}".format(call_back_url))
    result = func(*args)
    requests.post(call_back_url, json=result)


def process_in_background(data, data_loader):
    args = request.environ, data["call_back_endpoint"], server.federated_learning, data['type'], data_loader.X_test, data_loader.y_test, config
    Thread(target=async_processing, args=args).start()


@app.route('/async', methods=['POST'])
def train_model_async():
    data = request.get_json()
    logging.info("Initializing async model trainig acording to request {}".format(data))
    logging.info("host {} port {}".format(request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']))
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise ValueError(model_type)  # MODIFICAR
    data_loader = DataLoader()
    data_loader.load_data(5)
    process_in_background(data, data_loader)
    return jsonify("ok"), 200
