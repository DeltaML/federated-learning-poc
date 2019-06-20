import logging
from flask import request
from flask_restplus import Resource, Namespace, fields
from model_buyer.service.model_buyer import ModelBuyer


api = Namespace('models',  description='Model related operations')

features = api.model(name='Features', model={
    'list': fields.List(fields.String, required=True, description='The model type'),
    'range': fields.List(fields.Integer, required=True, description='The model type'),
    'pre_processing': fields.List(fields.Raw, required=False, description='The model type'),
    'desc': fields.Raw(required=False, description='The model type')
})

target = api.model(name='Target', model={
    'range': fields.List(fields.Integer, required=True, description='The model type'),
    'desc': fields.List(fields.String, required=True, description='The model type')
})

data_requirements = api.model(name='Data Requirements', model={
    'features': fields.Nested(features, required=True, description='The model type'),
    'target': fields.Nested(target, required=True, description='The model type'),
})


requirements = api.model(name='Requirements', model={
    'model_type': fields.String(required=True, description='The model type'),
    'testing_file_name': fields.String(required=True, description='The name of the file to test'),
    'data_requirements': fields.Nested(data_requirements, required=True, description='Data requirements')
})

model = api.model(name='Model', model={
    'status': fields.String(required=True, description='The model status'),
    'type': fields.String(required=True, description='The model type'),
    'weights': fields.List(fields.Raw, required=True, description='The model weights')
})


ordered_model = api.model(name='Ordered Model', model={
    'id': fields.String(required=True, description='The model identifier'),
    'requirements': fields.Nested(requirements, required=True, description='The model requirements'),
    'model': fields.Nested(model, required=True, description='The model')
})

model_request = api.model(name='Ordered Model Request', model={
    'data_requirements': fields.Nested(requirements, required=True, description='The model requirements'),
    'model_type': fields.String(required=True, description='The model type'),
    'initial_model': fields.Raw(required=False, description='The model type')
})


model_buyer = ModelBuyer()


@api.route('', endpoint='model_resources_ep')
class ModelResources(Resource):

    @api.expect(requirements, validate=True)
    @api.marshal_with(ordered_model, code=201)
    @api.doc('Create order model')
    def post(self):
        logging.info("New order model")
        data = request.get_json()
        return model_buyer.make_new_order_model(data), 200

    @api.marshal_list_with(ordered_model)
    def get(self):
        return model_buyer.models, 200


@api.route('/<model_id>', endpoint='model_ep')
@api.response(404, 'Model not found')
@api.param('model_id', 'The model identifier')
class ModelResource(Resource):

    @api.doc('put_model')
    @api.marshal_with(ordered_model)
    def put(self, model_id):
        data = request.get_json()
        return model_buyer.finish_model(model_id, data), 200

    @api.doc('patch_model')
    @api.marshal_with(ordered_model)
    def patch(self, model_id):
        data = request.get_json()
        return model_buyer.update_model(model_id, data), 200

    @api.doc('get_model')
    @api.marshal_with(ordered_model)
    def get(self, model_id):
        return model_buyer.get_model(model_id), 200


