import unittest
import numpy as np
from numpy import testing
from unittest.mock import MagicMock

from commons.decorators.decorators import optimized_collection_parameter, optimized_collection_response
from commons.decorators.decorators import normalize_optimized_collection_argument, normalize_optimized_response


class TestCashDecorator(unittest.TestCase):
    def test_optimized_collection_parameter_inactive(self):
        data = [1, 2, 3]
        ref = MagicMock()

        @optimized_collection_parameter(optimization=np.asarray, active=False)
        def a(p1, p2):
            return p2
        self.assertEqual(a(ref, data), data)
        self.assertFalse(testing.assert_array_equal(a(ref, data), np.asarray(data)))

    def test_optimized_collection_parameter_active(self):
        data = [1, 2, 3]
        ref = MagicMock()

        @optimized_collection_parameter(optimization=np.asarray, active=True)
        def a(p1, p2):
            return p2
        testing.assert_array_equal(a(ref, data), np.asarray(data))

    def test_optimized_collection_response_inactive(self):
        data = [1, 2, 3]
        ref = MagicMock()

        @optimized_collection_response(optimization=np.asarray, active=False)
        def a(p1, p2):
            return p2
        testing.assert_array_equal(a(ref, data), data)

    def test_optimized_collection_response_active(self):
        data = [1, 2, 3]
        ref = MagicMock()

        @optimized_collection_response(optimization=np.asarray, active=True)
        def a(p1, p2):
            return p2
        testing.assert_array_equal(a(ref, data), np.asarray(data))

    def test_normalize_optimized_collection_inactive(self):
        data = [1, 2, 3]
        np_data = np.asarray(data)
        ref = MagicMock()

        @normalize_optimized_collection_argument(active=False)
        def a(p1, p2, p3):
            return p3
        testing.assert_array_equal(a(ref, data, np_data), np_data)

    def test_normalize_optimized_collection_active(self):
        data = [1, 2, 3]
        np_data = np.asarray(data)
        ref = MagicMock()

        @normalize_optimized_collection_argument(active=True)
        def a(p1, p2, p3):
            return p3
        testing.assert_array_equal(a(ref, data, np_data), data)



    def test_normalize_optimized_response_inactive(self):
        data = [1, 2, 3]
        np_data = np.asarray(data)
        ref = MagicMock()

        @normalize_optimized_response(active=False)
        def a(p1, p2, p3):
            return p3
        testing.assert_array_equal(a(ref, data, np_data), np_data)

    def test_normalize_optimized_response_active(self):
        data = [1, 2, 3]
        np_data = np.asarray(data)
        ref = MagicMock()

        @normalize_optimized_response(active=True)
        def a(p1, p2, p3):
            return p3
        testing.assert_array_equal(a(ref, data, np_data), data)


