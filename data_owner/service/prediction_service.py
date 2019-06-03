class DataOwnerPrediction:

    def __init__(self, model_id, model_public_key, public_key, encrypted_prediction):
        self.id = encrypted_prediction.id
        self.model_id = model_id
        self.model_public_key = model_public_key
        self.public_key = public_key
        self.encrypted_prediction = encrypted_prediction
        self.confirmed = False
        self.is_valid = False

    def update(self, valid_status):
        self.is_valid = valid_status
        self.confirmed = True

    def get_data(self):
        return {'model_id': self.model_id,
                'prediction_id': self.id,
                'encrypted_prediction': self.encrypted_prediction.get_values(),
                'public_key': self.public_key}


class PredictionService:

    def __init__(self, encryption_service):
        self.predictions = dict()
        self.encryption_service = encryption_service

    def add(self, prediction_data):
        prediction = self._make_prediction(prediction_data)
        self.predictions[prediction.id] = prediction

    def get(self, prediction_id=None):
        return self.predictions.get(prediction_id) if prediction_id else self.predictions.values()

    def _make_prediction(self, prediction_data):
        return DataOwnerPrediction(model_id=prediction_data["model"]["model_id"],
                                   model_public_key=prediction_data["model"]["public_key"],
                                   public_key=self.encryption_service.get_public_key(),
                                   encrypted_prediction=prediction_data["encrypted_prediction"])

    def check_consistency(self, prediction_id, prediction_data):
        """

        :param prediction_id:
        :param prediction_data:
        :return:
        """
        prediction = self.get(prediction_id)
        #1) Decrypt -> (7)
        decrypted_prediction = self.encryption_service.decrypt_collection(prediction_data)
        #2) Encrypt with PK MB (8)
        encrypted_prediction = self.encryption_service.encrypt_collection(decrypted_prediction, prediction.model_public_key)
        #3) Compare 2) with (1)
        comparision = encrypted_prediction == prediction.encrypted_prediction
        prediction.update(prediction_data, comparision)
        return comparision


