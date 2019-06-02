import logging
import os
from logging.config import dictConfig

from flask import Flask, request, jsonify

from commons.data.data_loader import DataLoader
from commons.encryption.encryption_service import EncryptionService
from model_buyer.config import config, logging_config
from model_buyer.service.model_buyer import ModelBuyer

dictConfig(logging_config)


def create_app():
    # create and configure the app
    flask_app = Flask(__name__)
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    return flask_app


def build_data_loader():
    data_loader = DataLoader(config['DATASETS_DIR'])
    data_loader.load_data("data_test.csv")
    return data_loader


app = create_app()

logging.info("Model Buyer is running")

encryption_service = EncryptionService()
encryption_service.generate_key_pair(config["key_length"])

data_loader = build_data_loader()
model_buyer = ModelBuyer(encryption_service, data_loader, config)
model_training_id = []


## TODO: Refactor
def get_serialized_model(model):
    return {"requirements": model.requirements,
            "model": {"id": model.id,
                      "status": model.status.name,
                      "type": model.model_type,
                      "weights": model.get_weights()
                      }
            }


def get_serialized_prediction(prediction):
    return {"prediction_id": prediction.id, "values": prediction.get_values(), "mse": prediction.mse}

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
    model_buyer.finish_model(model_id, data)
    return jsonify(data), 200


@app.route('/model/<model_id>', methods=['PATCH'])
def partial_update_model(model_id):
    data = request.get_json()
    model_buyer.update_model(model_id, data)
    return jsonify(data), 200


@app.route('/model', methods=['GET'])
def get_models():
    return jsonify([get_serialized_model(model) for model in model_buyer.models]), 200


@app.route('/model/<model_id>', methods=['GET'])
def get_model(model_id):
    model = model_buyer.get_model(model_id)
    return jsonify(get_serialized_model(model)), 200


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
    logging.info(file)
    file.save('./dataset/data.csv')
    file.close()
    return jsonify(200)


@app.route('/ping', methods=['POST'])
def ping():
    return jsonify("pong")
