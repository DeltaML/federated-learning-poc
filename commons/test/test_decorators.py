import unittest
import numpy as np
from numpy import testing
from unittest.mock import MagicMock

from commons.decorators.decorators import optimized_collection_parameter


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


