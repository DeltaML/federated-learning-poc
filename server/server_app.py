import logging
import sys, os
from logging.config import dictConfig
from flask import Flask, request, jsonify
from operations_utils.functions import get_encrypted_number, get_deserialized_public_key, get_serialized_gradient
from requests import post
from Server import Server
from ClientInstance import ClientInstance

pub_key = "92951797244797167983167141550409296171197189592094991997506301474877894634359396591953594500920983392267035342569100192517151963310836036953999162112864331801677221081621985971954201113862653384753921706561342038828618807924079228073528307264707630640359846482233951074062256062688524495232625357433668057413"

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
    new_client = ClientInstance(data, pub_key)
    server.register_client(new_client)
    return jsonify(str(new_client))


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
    logging.info("process_weights with {}".format(data))
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise InvalidModelException(model_type)
    #server.federated_learning()
    response = "hola"
    return jsonify(response)
