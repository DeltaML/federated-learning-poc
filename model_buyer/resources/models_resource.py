import logging
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from model_buyer.service.model_buyer import ModelBuyer

api = Namespace('models', description='Model related operations')

requirements = api.model('requirements Model', {
    'id': fields.String(required=True, description='The model identifier')
})

model = api.model('Model', {
    'status': fields.String(required=True, description='The model status'),
    'type': fields.String(required=True, description='The model type'),
    'weights': fields.List(fields.Raw, required=True, description='The model weights')
})


ordered_model = api.model('Ordered Model', {
    'id': fields.String(required=True, description='The model identifier'),
    'requirements': fields.Nested(requirements, required=True, description='The model requirements'),
    'model': fields.Nested(model, required=True, description='The model')
})

model_buyer = ModelBuyer()


# TODO: Refactor
def get_serialized_model(model):
    return {"requirements": model.requirements,
            "model": {"id": model.id,
                      "status": model.status.name,
                      "type": model.model_type,
                      "weights": model.get_weights()
                      }
            }


@api.route('', endpoint='model_resources_ep')
class ModelResources(Resource):

    @api.marshal_with(ordered_model, code=201)
    @api.doc('Create order model')
    def post(self):
        logging.info("Make new order")
        data = request.get_json()
        order = model_buyer.make_new_order_model(data)
        return jsonify(order), 200

    @api.marshal_list_with(ordered_model)
    def get(self):
        return jsonify([get_serialized_model(model) for model in model_buyer.models]), 200


@api.route('/<model_id>', endpoint='model_ep')
@api.response(404, 'Model not found')
@api.param('model_id', 'The model identifier')
class ModelResource(Resource):


    @api.doc('put_model')
    @api.marshal_with(ordered_model)
    def put(self, model_id):
        data = request.get_json()
        model_buyer.finish_model(model_id, data)
        return jsonify(data), 200

    @api.doc('patch_model')
    @api.marshal_with(ordered_model)
    def patch(self, model_id):
        data = request.get_json()
        model_buyer.update_model(model_id, data)
        return jsonify(data), 200

    @api.doc('patch_model')
    @api.marshal_with(ordered_model)
    def get(self, model_id):
        model = model_buyer.get_model(model_id)
        return jsonify(get_serialized_model(model)), 200

