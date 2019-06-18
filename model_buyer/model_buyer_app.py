import logging
import os
import random
from logging.config import dictConfig

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from commons.data.data_loader import DataLoader
from commons.encryption.encryption_service import EncryptionService
from model_buyer.service.model_buyer import ModelBuyer
from model_buyer.resources import api

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
    flask_app = Flask(__name__, static_folder='ui/build/')
    flask_app.config.from_pyfile('config.py')
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    return flask_app


def build_data_loader():
    data_loader = DataLoader(app.config['DATASETS_DIR'])
    data_loader.load_data("data_test.csv")
    return data_loader

app = create_app()
api.init_app(app)

CORS(app)
logging.info("Model Buyer is running")

encryption_service = EncryptionService()
public_key, private_key = encryption_service.generate_key_pair(app.config["KEY_LENGTH"])
encryption_service.set_public_key(public_key.n)
data_loader = DataLoader(app.config['DATASETS_DIR'])
model_buyer = ModelBuyer().init(encryption_service, data_loader, app.config)
model_training_id = []


def get_serialized_prediction(prediction):
    return {"prediction_id": prediction.id, "values": prediction.get_values(), "mse": prediction.mse,
            "model": get_serialized_model(prediction.model)}


# TODO: Refactor
def get_serialized_model(model):
    return {"requirements": model.requirements,
            "model": {"id": model.id,
                      "status": model.status.name,
                      "type": model.model_type,
                      "weights": model.get_weights()
                      }
            }


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


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/transform', methods=['POST'])
def transform_prediction():
    logging.info("transform prediction from data owner")
    model_buyer.transform_prediction(request.get_json())
    return jsonify(200), 200


@app.route('/prediction', methods=['POST'])
def make_prediction():
    data = request.get_json()
    prediction = model_buyer.make_prediction(data)
    return jsonify(get_serialized_prediction(prediction)), 200


@app.route('/prediction', methods=['GET'])
def get_predictions():
    return jsonify([get_serialized_prediction(prediction) for prediction in model_buyer.predictions]), 200


@app.route('/prediction/<prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    prediction = model_buyer.get_prediction(prediction_id)
    return jsonify(get_serialized_prediction(prediction)), 200


@app.route('/dataset', methods=['POST'])
def load_dataset():
    file = request.files.get('file')
    filename = request.files.get('filename') or file.filename
    logging.info(file)
    file.save('./dataset/{}'.format(filename))
    file.close()
    return jsonify(200)


@app.route('/ping', methods=['GET'])
def ping():
    response = {
        "values": [1, 2, 3],
        "MSE": random.randint(1, 2)
    }
    return jsonify(response)
