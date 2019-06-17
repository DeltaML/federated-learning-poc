import logging
import os
from flask import Flask, request, jsonify

from commons.encryption.encryption_service import EncryptionService
from federated_trainer.service.federated_trainer import FederatedTrainer

from logging.config import dictConfig

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
    # load the instance config
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    flask_app.config.from_pyfile('config.py')
    return flask_app


app = create_app()
encryption_service = EncryptionService()
federated_trainer = FederatedTrainer(encryption_service=encryption_service, config=app.config)
logging.info("federated_trainer running")


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


@app.route('/dataowner', methods=['POST'])
def register_data_owner():
    # Json contiene url y puerto a donde esta el cliente que se esta logueando
    data = request.get_json()
    data["host"], data["port"] = request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']
    response = federated_trainer.register_data_owner(data)
    return jsonify(response)


@app.route('/dataowner', methods=['GET'])
def get_data_owners():
    return jsonify([str(data_owner) for data_owner in federated_trainer.data_owners])


@app.route('/model', methods=['POST'])
def train_model_async():
    data = request.get_json()
    logging.info("Initializing async model training according to request {}".format(data))
    logging.info("host {} port {}".format(request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT']))
    # Validate model type
    federated_trainer.process(request.environ['REMOTE_ADDR'], data)
    return jsonify(200)


@app.route('/prediction', methods=['POST'])
def post_prediction():
    data = request.get_json()
    logging.info("Data {}".format(data))
    federated_trainer.send_prediction_to_buyer(data)
    return jsonify(200), 200


@app.route('/prediction/<prediction_id>', methods=['PATCH'])
def patch_prediction(prediction_id):
    data = request.get_json()
    logging.info("Data {}".format(data))
    federated_trainer.send_prediction_to_data_owner(data)
    return jsonify("pong")




@app.route('/ping', methods=['POST'])
def ping():
    logging.info("Data {}".format(request.get_json()))
    return jsonify("pong")
