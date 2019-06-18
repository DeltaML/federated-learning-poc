import logging
from flask import jsonify, make_response
from flask_restplus import Api

from model_buyer.resources.models_resource import api as model_api

api = Api(
    title='Model Buyer Api',
    version='1.0',
    description='Model Buyer Api API',
    doc='/doc/'
)

api.add_namespace(model_api)


@api.errorhandler(Exception)
def default_error_handler(error):
    """
    Default error handler
    :param error:
    :return:
    """
    logging.error(error)
    return {'message': str(error)}, getattr(error, 'code', 500)


def _handle_error(error):
    logging.error(error)
    return ErrorHandler.create_error_response(error.status_code, error.message)


class ErrorHandler:
    @staticmethod
    def create_error_response(status_code, message):
        return make_response(
            jsonify(
                {
                    "status_code": status_code,
                    "message": message
                }
            ),
            status_code
        )
