import unittest
from unittest.mock import MagicMock
import json

from data_owner.service.decorators import serialize_encrypted_data, serialize_encrypted_model_data, \
    serialize_encrypted_model_data


class TestDataOwnerDecorator(unittest.TestCase):
    def test_serialize_encrypted_data_inactive(self):
        data = str([1, 2, 3])
        ref = MagicMock()
        encryption_service = MagicMock()

        @serialize_encrypted_data(encryption_service=encryption_service, schema=json.loads, active=False)
        def func(p1, p2):
            return p2

        self.assertEqual(func(ref, data), json.loads(data))

    def test_serialize_encrypted_data_active(self):
        data = str([1, 2, 3])
        ref = MagicMock()
        encryption_service = MagicMock()
        encryption_service.get_serialized_encrypted_collection = MagicMock(return_value=data)

        @serialize_encrypted_data(encryption_service=encryption_service, schema=json.loads, active=True)
        def func(p1, p2):
            return p2

        self.assertEqual(func(ref, data), json.loads(data))
        encryption_service.get_serialized_encrypted_collection.assert_called_with(data)
