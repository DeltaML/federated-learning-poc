import logging
from flask import request
from flask_restplus import Resource, Namespace, fields
from model_buyer.service.model_buyer import ModelBuyer


api = Namespace('predictions', description='Predictions related operations')


prediction = api.model(name='Prediction ', model={
    'id': fields.String(required=True, description='The prediction identifier'),
    'values': fields.List(fields.Raw, required=True, description='The prediction values'),
    'mse': fields.Integer(required=True, description='The MSE'),
 #   'model': fields.Nested(model, required=True, description='The model'),
})


prediction_request = api.model(name='Prediction ', model={
    'id': fields.String(required=True, description='The prediction identifier')
})


model_buyer = ModelBuyer()


@api.route('', endpoint='predictions')
@api.doc('Prediction resources')
class PredictionsResources(Resource):

    @api.expect(prediction_request, validate=True)
    @api.marshal_with(prediction, code=201)
    @api.doc('Create prediction')
    def post(self):
        logging.info("Make new prediction")
        data = request.get_json()
        return model_buyer.make_prediction(data), 200

    @api.marshal_list_with(prediction)
    @api.doc('Get predictions')
    def get(self):
        return model_buyer.predictions, 200


@api.route('/<prediction_id>', endpoint='prediction_ep')
@api.response(404, 'Prediction not found')
@api.param('prediction_id', 'The prediction identifier')
@api.doc('Prediction resource')
class PredictionResource(Resource):

    @api.marshal_with(prediction)
    @api.doc('get prediction')
    def get(self, prediction_id):
        return model_buyer.get_prediction(prediction_id), 200
