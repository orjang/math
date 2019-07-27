import unittest
from pymath.vector import Vector


class TestVector(unittest.TestCase):

    def test_can_create_vector(self):
        v = Vector([1, 2, 3])
        self.assertEqual(len(v), 3)

    def test_can_index_vector(self):
        v = Vector([1, 2, 3])
        self.assertEqual(v[0], 1)
        self.assertEqual(v[1], 2)
        self.assertEqual(v[2], 3)

    def test_vector_is_elementwise_compared_with_list(self):
        v = Vector([1, 2, 3])
        self.assertTrue(v == [1, 2, 3])
        self.assertFalse(v == [3, 2, 1])

    def test_can_add_two_vectors_of_equal_length(self):
        a = Vector([1, 2, 3])
        b = Vector([3, 2, 1])
        c = a + b
        self.assertEqual(c, [4, 4, 4])

    def test_can_not_add_two_vectors_of_unequal_length(self):
        def add_vectors(a, b):
            return a + b
        v1 = Vector([1, 2, 3])
        v2 = Vector([1])
        self.assertRaises(ValueError, add_vectors, v1, v2)

    def test_vector_can_be_multiplied_by_scalar(self):
        v = Vector([1, 2, 3])
        v2 = v * 5
        self.assertEqual(v2, [5, 10, 15])
        v2 = 2 * v
        self.assertEqual(v2, [2, 4, 6])


