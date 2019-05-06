import logging
import os

from logging.config import dictConfig
from flask import Flask, request, jsonify
from commons.encryption.encryption_service import EncryptionService
from model_buyer.config import config
from model_buyer.service.model_buyer import ModelBuyer

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
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    return flask_app


app = create_app()
logging.info("Model Buyer is running")

encryption_service = EncryptionService()
public_key, private_key = encryption_service.generate_key_pair(config["key_length"])
encryption_service.set_public_key(public_key.n)
model_buyer = ModelBuyer(public_key, private_key, encryption_service, config)


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


@app.route('/model', methods=['POST'])
def make_order_model():
    logging.info("Make new order")
    data = request.get_json()
    order = model_buyer.make_new_order_model(data)
    return jsonify(order), 200


@app.route('/model/<model_id>', methods=['PUT'])
def update_model(model_id):
    data = request.get_json()
    model_buyer.update_model(model_id, data)
    return jsonify(data), 200


@app.route('/model/<model_id>', methods=['GET'])
def get_model(model_id):
    return jsonify(model_buyer.get_model(model_id)), 200


@app.route('/prediction', methods=['POST'])
def make_prediction():
    data = request.get_json()
    prediction = model_buyer.make_prediction(data)
    return jsonify(prediction), 200


@app.route('/prediction/<predition_id>', methods=['GET'])
def make_prediction(predition_id):
    prediction = model_buyer.get_prediction(predition_id)
    return jsonify(prediction), 200


@app.route('/ping', methods=['POST'])
def ping():
    return jsonify("pong")

