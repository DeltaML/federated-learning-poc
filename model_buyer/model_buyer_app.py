import logging
import os
import requests

from logging.config import dictConfig
from flask import Flask, request, jsonify
from commons.data.data_loader import DataLoader
from commons.encryption.encryption_service import EncryptionService
from commons.encryption.phe_encryption import PheEncryption
from commons.model.model_service import ModelFactory, ModelType
from commons.operations_utils.functions import mean_square_error

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
    'port': 9090,
    'active_encryption': False,
    'encryption_type': PheEncryption
}

encryption_service = EncryptionService(config["encryption_type"]())
public_key, private_key = encryption_service.generate_key_pair(config["key_length"])
encryption_service.set_public_key(public_key.n)


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

X_train, y_train, X_test, y_test = DataLoader().load_random_data()
model = ModelFactory.get_model(ModelType.LINEAR_REGRESSION.name)(X_train, y_train)


# Single endpoints
@app.route('/finished', methods=['POST'])
def finished():
    # Json contiene url y puerto a donde esta el cliente que se esta logueando
    data = request.get_json()
    logging.info("DATA Encrypted{}".format(data))
    d_data = encryption_service.decrypt_and_deserizalize_collection(private_key, data) if config["active_encryption"] else data
    logging.info("DATA Dencryted{}".format(d_data))
    model.set_weights(d_data)
    return jsonify(data), 200


@app.route('/model', methods=['POST'])
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


@app.route('/prediction', methods=['GET'])
def get_prediction():
    y_pred = model.predict(X_test)
    mse = mean_square_error(y_pred, y_test)
    return jsonify({'pred': y_pred.tolist(), 'mse': mse})
