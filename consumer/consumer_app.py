import logging
import os
from logging.config import dictConfig
from flask import Flask, request, jsonify
import requests

from commons.encryption.encryption_service import EncryptionService
from commons.encryption.phe_encryption import PheEncryption

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
    'server_register_url': "http://localhost:8080/model",
    'key_length': 1024,
    'port': 9090
}

encryption_service = EncryptionService(PheEncryption())
public_key, private_key = encryption_service.generate_key_pair(config["key_length"])


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
logging.info("Consumer running")


# Single endpoints
@app.route('/finished', methods=['POST'])
def register_client():
    # Json contiene url y puerto a donde esta el cliente que se esta logueando
    data = request.get_json()
    logging.info("DATA {}".format(data))
    return jsonify(data), 200


@app.route('/predict', methods=['POST'])
def predict():
    logging.info("init predict")
    data = dict(type="LINEAR_REGRESSION",
                call_back_endpoint="finished",
                call_back_port=config["port"],
                public_key=public_key.n)
    response = requests.post(config["server_register_url"], json=data)
    response.raise_for_status()
    return jsonify("init predict")


@app.route('/ping', methods=['POST'])
def ping():
    return jsonify("pong")
