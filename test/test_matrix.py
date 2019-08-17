import unittest
from pymath.matrix import Matrix


class Initialization(unittest.TestCase):

    @staticmethod
    def test_can_create_default_matrix():
        v = Matrix(3, 3)

    def test_default_created_matrix_has_correct_number_of_rows(self):
        v = Matrix(3, 1)
        self.assertEqual(v.shape.rows, 3)

    def test_default_created_matrix_has_correct_number_of_columns(self):
        v = Matrix(3, 1)
        self.assertEqual(v.shape.columns, 1)

    @staticmethod
    def test_all_entries_can_be_indexed():
        v = Matrix(4, 3)
        for r in range(v.shape.rows):
            for c in range(v.shape.columns):
                _ = v[r, c]

    def test_all_elements_can_be_assigned_to(self):
        v = Matrix(3, 4)
        for r in range(v.shape.rows):
            for c in range(v.shape.columns):
                val = r * v.shape.columns + c
                v[r, c] = val
                self.assertEqual(v[r, c], val)

    def test_default_matrix_is_the_zero_matrix(self):
        v = Matrix(3, 3)
        for r in range(v.shape.rows):
            for c in range(v.shape.columns):
                entry = v[r, c]
                self.assertAlmostEqual(entry, 0, msg='entry({}, {}) is not 0'.format(r, c))

    def test_can_create_matrix_initialized_from_list_of_lists(self):
        v = Matrix([[0, 1, 2], [3, 4, 5]])
        self.assertEqual(v.shape, (2, 3))
        for r in range(v.shape.rows):
            for c in range(v.shape.columns):
                self.assertEqual(r * v.shape.columns + c, v[r, c])

    def test_rows_or_columns_of_list_of_lists_data_initializer_must_not_be_empty(self):
        with self.assertRaises(ValueError, msg='Matrix accepts initializer with empty columns'):
            m = Matrix([[], []])
        with self.assertRaises(ValueError, msg='Matrix accepts initializer with empty rows'):
            m = Matrix([])

    def test_column_sizes_must_be_consistent_when_initialized_from_list_of_lists(self):
        with self.assertRaises(ValueError, msg='Matrix accepts initializer with inconsistent column sizes'):
            m = Matrix([[0, 1, 2], [3, 4]])

    def test_can_create_matrix_initialized_from_list_and_dimensions(self):
        v = Matrix([0, 1, 2, 3, 4, 5], 2, 3)
        self.assertEqual(v.shape, (2, 3))
        for r in range(v.shape.rows):
            for c in range(v.shape.columns):
                self.assertEqual(r * v.shape.columns + c, v[r, c])

    def test_data_initializer_for_matrix_initialized_from_list_and_dimensions_must_have_exactly_rows_times_columns_entries(self):
        v = Matrix([0, 1], 1, 2)
        v = Matrix([0, 1, 2], 1, 3)
        v = Matrix([0, 1, 2, 3], 2, 2)
        with self.assertRaises(ValueError, msg='Matrix accepts initializer with too few entries'):
            v = Matrix([0, 1], 1, 3)
        with self.assertRaises(ValueError, msg='Matrix accepts initializer with too many entries'):
            v = Matrix([0, 1, 3, 4], 1, 3)

    def test_initialize_from_matrix_instance_gives_a_deep_copy(self):
        a = Matrix([0, 1, 2, 3], 1, 4)
        ap = Matrix([0, 1, 2, 3], 1, 4)
        b = Matrix(a)

        self.assertEqual(a, b)
        b[0, 0] = 42
        self.assertEqual(a[0, 0], 0)
        self.assertEqual(b[0, 0], 42)
        self.assertEqual(a, ap)
        self.assertNotEqual(a, b)


class Comparisons(unittest.TestCase):

    def test_matrix_elements_can_be_assigned_with_a_slice(self):
        m = Matrix(3, 3)
        m[0] = [1, 2, 3]
        self.assertEqual([1, 2, 3], m[0])

    def test_can_only_compare_with_other_matrices(self):
        m = Matrix(2, 2)
        with self.assertRaises(TypeError, msg='Matrices can only be compared with other matrices'):
            m == 42

    def test_two_matrices_can_be_compared_for_equality(self):
        m1 = Matrix([[0], [1], [2], [3]])
        m2 = Matrix([0, 1, 2, 3], 4, 1)
        m3 = Matrix([0, 1, 2, 3], 1, 4)
        m4 = Matrix([[0, 1, 2, 3]])
        self.assertEqual(m1, m2)
        self.assertEqual(m3, m4)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, m4)
        self.assertNotEqual(m2, m3)
        self.assertNotEqual(m2, m4)


class Arithmetic(unittest.TestCase):

    def test_matrices_of_same_dimensions_can_be_added(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[4, 3], [2, 1]])
        expected = Matrix([[5, 5], [5, 5]])
        m = m1 + m2
        self.assertEqual(expected, m)

    def test_matrices_of_different_dimensions_can_not_be_added(self):
        m1 = Matrix([[1, 2, 3, 4]])
        m2 = Matrix([[4, 3], [2, 1]])
        with self.assertRaises(ValueError, msg='Matrices with non matching dimensions can\'t be added'):
            m = m1 + m2

    def test_matrices_of_same_dimensions_can_be_subtracted(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[4, 3], [2, 1]])
        expected = Matrix([[-3, -1], [1, 3]])
        m = m1 - m2
        self.assertEqual(expected, m)

    def test_matrices_of_different_dimensions_can_not_be_subtracted(self):
        m1 = Matrix([[1, 2, 3, 4]])
        m2 = Matrix([[4, 3], [2, 1]])
        with self.assertRaises(ValueError, msg='Matrices with non matching dimensions can\'t be subtracted'):
            m = m1 - m2

    def test_matrix_can_be_multiplied_by_a_number(self):
        m1 = Matrix([[1, 2, 3, 4]])
        expected = Matrix([[10, 20, 30, 40]])

        m = m1 * 10.
        self.assertEqual(expected, m)

    def check_product(self, m1, m2, expected):
        m = m1 @ m2
        self.assertEqual(expected, m)

    def test_matrices_with_matching_inner_dimension_can_be_multiplied(self):
        self.check_product(Matrix([[2], [1]]), Matrix([[1, 2]]), Matrix([[2, 4], [1, 2]]))
        self.check_product(Matrix([[1, 2]]), Matrix([[2], [1]]), Matrix([[4]]))
        self.check_product(
            Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]]),
            Matrix([[30,  24,  18], [84,  69,  54], [138, 114,  90]])
        )

    def test_matrices_must_have_same_inner_dimension_to_multiply(self):
        with self.assertRaises(ValueError, msg='Matrix product accepts incompatible matrices'):
            Matrix([[1, 2]]) @ Matrix([[1, 2]])


class Functions(unittest.TestCase):
    def test_row(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        r0 = m.row(0)
        r1 = m.row(1)
        r2 = m.row(2)
        self.assertEqual([1, 2, 3], r0)
        self.assertEqual([4, 5, 6], r1)
        self.assertEqual([7, 8, 9], r2)

    def test_column(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        c0 = m.column(0)
        c1 = m.column(1)
        c2 = m.column(2)
        self.assertEqual([1, 4, 7], c0)
        self.assertEqual([2, 5, 8], c1)
        self.assertEqual([3, 6, 9], c2)

    def test_matrix_transpose(self):
        def check_transpose(morig):
            mtr = morig.T
            odim, tdim = morig.shape, mtr.shape
            self.assertEqual((odim.rows, odim.columns), (tdim.columns, tdim.rows))
            self.assertEqual(morig, morig.T.T)

            for r in range(odim.rows):
                for c in range(odim.columns):
                    self.assertEqual(morig[r, c], mtr[c, r])

        check_transpose(Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        check_transpose(Matrix([[1, 2, 3], [4, 5, 6]]))
        check_transpose(Matrix([[1, 2, 3]]))
        check_transpose(Matrix([[1], [2], [3]]))
        check_transpose(Matrix([[1]]))


class MatrixAddition(unittest.TestCase):
    def test_is_commutative(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[4, 3], [2, 1]])
        self.assertEqual(a+b, b+a)

    def test_is_associative(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[4, 3], [2, 1]])
        c = Matrix([[3, 4], [1, 2]])
        self.assertEqual(a+(b+c), (a+b)+c)

    def test_additive_identity(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix(*a.shape)
        self.assertEqual(a, a+b)


class ScalarMultiplication(unittest.TestCase):
    def test_multiplicative_zero(self):
        a = Matrix([[4, 3], [2, 1]])
        z = Matrix(2, 2)

        self.assertEqual(z, a*0)
        self.assertEqual(z, 0*a)

    def test_multiplicative_identity(self):
        a = Matrix([[4, 3], [2, 1]])

        self.assertEqual(a, a*1)
        self.assertEqual(a, 1*a)

    def test_is_distributive(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[4, 3], [2, 1]])
        n = 42
        m = 24
        self.assertEqual(n*(a+b), n*a + n*b)
        self.assertEqual((n+m)*a, n*a + m*a)

    def test_is_associative(self):
        a = Matrix([[1, 2], [3, 4]])
        n = 42
        m = 24
        self.assertEqual((n*m)*a, n*(m*a))

    def test_is_commutative(self):
        a = Matrix([[1, 2], [3, 4]])
        n = 42
        self.assertEqual(n*a, a*n)


class MatrixMultiplication(unittest.TestCase):
    def test_multiplicative_zero(self):
        a = Matrix([[4, 3], [2, 1]])
        z = Matrix(2, 2)

        self.assertEqual(z, a*z)

    def test_multiplicative_identity(self):
        a = Matrix([[4, 3], [2, 1]])
        I = Matrix.identity(2, float)

        self.assertEqual(a, a*I)

    def test_is_associative(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[4, 3], [2, 1]])
        c = Matrix([[3, 4], [1, 2]])

        self.assertEqual(a*(b*c), (a*b)*c)

    def test_is_distributive(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[4, 3], [2, 1]])
        c = Matrix([[3, 4], [1, 2]])

        self.assertEqual((a+b)*c, a*c + b*c)
        self.assertEqual(c*(a+b), c*a + c*b)
        self.assertEqual((a*b)*c, a*(b*c))

    def test_associative_over_scalar_multiplication(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[4, 3], [2, 1]])
        n = 42

        self.assertEqual((n*a)*b, a*(n*b))
        self.assertEqual((n*a)*b, n*(a*b))


class ElementaryOperations(unittest.TestCase):
    def test_can_swap_two_rows(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m = m.exchange_rows(0, 1)

        self.assertEqual(m, Matrix([[4, 5, 6], [1, 2, 3], [7, 8, 9]]))
