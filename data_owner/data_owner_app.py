import logging
import os
from logging.config import dictConfig
from flask import Flask, request, jsonify
from data_owner.service.data_owner import DataOwnerFactory
from commons.data.data_loader import DataLoader

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


# Global variables
app = create_app()
data_loader = DataLoader(app.config["DATASETS_DIR"])
data_owner = DataOwnerFactory.create_data_owner(app.config, data_loader)
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
    filename = request.files.get('filename') or file.filename
    logging.info(file)
    file.save('./dataset/{}'.format(filename))
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


@app.route('/model/train/', methods=['POST'])
def train():
    data = request.get_json()
    id, gradient = data_owner.train(data['model_type'], data['weights'])
    return {'data_owner': id, 'update': gradient}


@app.route('/weights', methods=['POST'])
def compute_gradient():
    """
    process weights from server
    :return:
    """
    logging.info("Process weights")
    data = request.get_json()
    id, gradient = data_owner.process(data['model_type'], data['weights'])
    return jsonify({'data_owner': id, 'update': gradient})


@app.route('/step', methods=['PUT'])
def gradient_step():
    """
    Execute step with gradient
    :return:
    """
    data = request.get_json()
    logging.info("Gradient step")
    data_owner.step(data["gradient"])
    return jsonify(200)


@app.route('/model', methods=['GET'])
def get_model():
    logging.info("Get Model")
    return data_owner.get_model()


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(200)


@app.route('/data/requirements', methods=['POST'])
def link_reqs_to_file():
    data = request.get_json()
    training_req_id = data['model_id']
    reqs = data['requirements']['data_requirements']
    result = data_owner.link_dataset_to_model_id(training_req_id, reqs)
    return jsonify({training_req_id: (data_owner.client_id, result)})


@app.route('/model/metrics', methods=['POST'])
def get_model_quality():
    data = request.get_json()
    model_id = data["model_id"]
    model_type = data["model_type"]
    weights = data["model"]
    logging.info("Getting metrics, data owner: {}".format(data_owner.client_id))
    return jsonify(data_owner.model_quality_metrics(model_type, weights))






