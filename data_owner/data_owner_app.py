import logging
import os
from logging.config import dictConfig
from flask import Flask, request, jsonify
from data_owner.service.data_owner_service import DataOwnerFactory
from commons.data.data_loader import DataLoader
from data_owner.service.decorators import serialize_encrypted_data, deserialize_encrypted_data, \
    serialize_encrypted_model_data
from commons.encryption.encryption_service import EncryptionService
from flask import send_from_directory

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
    # load the instance config
    flask_app.config.from_pyfile('config.py')
    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    return flask_app


def build_data_loader(config):
    data_loader = DataLoader()
    #data_loader.load_data() #config['N_SEGMENTS'])
    return data_loader


def build_encryption_service(config):
    encryption_type = config['ENCRYPTION_TYPE']
    return EncryptionService(encryption_type())


# Global variables
app = create_app()
data_loader = build_data_loader(app.config)
encryption_service = build_encryption_service(app.config)
data_owner = DataOwnerFactory.create_data_owner(app.config, data_loader, encryption_service)
active_encryption = app.config["ACTIVE_ENCRYPTION"]


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/dataset', methods=['POST'])
def load_dataset():
    file = request.files.get('file')
    logging.info(file)
    file.save('./dataset/data.csv')
    file.close()
    return jsonify(200)


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


@app.route('/weights', methods=['POST'])
@serialize_encrypted_data(encryption_service=encryption_service, schema=jsonify, active=active_encryption)
def process_weights():
    """
    process weights from server
    :return:
    """
    logging.info("Process weights")
    data = request.get_json()
    # model type
    model_type = data['type']
    # encrypted_model
    return data_owner.process(model_type, data["public_key"])


@app.route('/step', methods=['PUT'])
@deserialize_encrypted_data(encryption_service=encryption_service, request=request, active=active_encryption)
def gradient_step(data):
    """
    Execute step with gradient
    :return:
    """
    logging.info("Gradient step")
    data_owner.step(data)
    return jsonify(200)


@app.route('/model', methods=['GET'])
@serialize_encrypted_model_data(encryption_service=encryption_service, schema=jsonify, active=active_encryption)
def get_model():
    logging.info("Get Model")
    return data_owner.get_model()


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(200)

