import logging
import os
import random
from logging.config import dictConfig

from flask import Flask, request, jsonify, send_from_directory, flash, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

from commons.data.data_loader import DataLoader
from commons.encryption.encryption_service import EncryptionService
from model_buyer.service.model_buyer import ModelBuyer
from model_buyer.resources import api
from model_buyer.config.logging_config import DEV_LOGGING_CONFIG, PROD_LOGGING_CONFIG


UI_PATH = 'ui/build/'


def create_app():
    # create and configure the app
    flask_app = Flask(__name__, static_folder=UI_PATH)
    if 'ENV_PROD' in os.environ and os.environ['ENV_PROD']:
        flask_app.config.from_pyfile("config/prod/app_config.py")
        dictConfig(PROD_LOGGING_CONFIG)
    else:
        dictConfig(DEV_LOGGING_CONFIG)
        flask_app.config.from_pyfile("config/dev/app_config.py")

    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    return flask_app


app = create_app()
api.init_app(app)

CORS(app)
logging.info("Model Buyer is running")

encryption_service = EncryptionService()
public_key, private_key = encryption_service.generate_key_pair(app.config["KEY_LENGTH"])
encryption_service.set_public_key(public_key.n)
data_loader = DataLoader(app.config['DATA_SETS_DIR'])
model_buyer = ModelBuyer()
model_buyer.init(encryption_service, data_loader, app.config)


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


@app.route('/file', methods=['POST'])
def load_data_set():
    """
    :return:
    """
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    filename = secure_filename(file.filename)
    model_buyer.load_data_set(file, filename)
    return jsonify(200)


@app.route('/ping', methods=['GET'])
def ping():
    response = {
        "values": [1, 2, 3],
        "MSE": random.randint(1, 2)
    }
    return jsonify(response)
