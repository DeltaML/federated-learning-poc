import logging
import os
from logging.config import dictConfig
from flask import Flask, request, jsonify
from commons.data.data_loader import DataLoader
from exceptions.exceptions import InvalidModelException
from service.client_service import ClientFactory
from service.model_service import ModelType
from flask import send_from_directory
import numpy as np

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
    flask_app = Flask(__name__, static_folder='ui/build/', instance_relative_config=True)
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
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
  next()
})
data_loader = DataLoader()
data_loader.load_data(app.config['N_SEGMENTS'])
X_client = None
y_client = None
client = ClientFactory.create_client(app.config, data_loader)
client.register(app.config['N_SEGMENTS'])
logging.info("Register Number" + str(client.register_number))


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
    form = request.form
    files =  request.files
    logging.info(request)
    logging.info(form)
    logging.info(files)
    logging.info(form.get('file'))
    logging.info(files.get('file'))
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
def process_weights():
    """
    process weights from server
    :return:
    """
    data = request.get_json()
    #logging.info("process_weights with {}".format(data))
    # Validate model type
    model_type = data['type']
    if not ModelType.validate(model_type):
        raise InvalidModelException(model_type)
    # encrypted_model
    response = client.process(model_type)
    return jsonify(response)


@app.route('/step', methods=['PUT'])
def gradient_step():
    data = request.get_json()
    client.step(np.asarray(data["gradient"]))
    return jsonify(200)

@app.route('/model', methods=['GET'])
def getModel():
    return jsonify(client.model.weights.tolist())


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(200)
