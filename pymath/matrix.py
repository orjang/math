import collections


def argmax(lst, begin=0):
    """Helper function to get index of first max entry of a list"""
    return max(range(begin, len(lst)), key=lambda i: abs(lst[i]))


MatrixShape = collections.namedtuple('MatrixShape', ['rows', 'columns'])


def _check_operand_types(lhs, rhs, operand):
    if not (isinstance(rhs, Matrix) and isinstance(lhs, Matrix)):
        raise TypeError("unsupported operand type for '{}}': {}/{}".format(type(lhs), type(rhs), operand))


def _check_equal_shape(lhs, rhs):
    if lhs.shape != rhs.shape:
        raise ValueError('matrix shapes not equal')


def _check_equal_inner_dimensions(lhs, rhs):
    if lhs.shape.columns != rhs.shape.rows:
        raise ValueError('matrices inner dimension does not match')


class Matrix(object):
    """A class implementing a 2-dimensional matrix usable for linear algebra

      Can be created in three different ways:
       - Default created, all entries is initialized to 0
         This will create a matrix with 3 rows of 2 columns each:
           m = Matrix(3, 2)

       - With initial data in the form of a list-of-lists (or any iterable with two dimensions)
         This will create a 3 by 3 matrix where first row is 1,2,3 and so on.
            m = Matrix([[1,2,3], [4,5,6], [7,8,9]])

       - With initial data in the form of a list (or any iterable) and number of rows and columns specified
           m = Matrix([1,2,3,4], 2, 2)
    """

    def __init__(self, *args, dtype=float):
        nargs = len(args)
        self.dtype = dtype
        if nargs == 1 and isinstance(args[0], Matrix):
            self._init_from_other_matrix(args[0])
        elif nargs == 1 and hasattr(args[0], '__iter__'):
            self._init_from_list_of_lists(args[0], dtype)
        elif nargs == 3 and hasattr(args[0], '__iter__'):
            self._init_from_single_list(args[0], args[1], args[2], dtype)
        else:
            rows, cols = args
            self._shape = MatrixShape(rows, cols)
            self._data = [dtype(0) for _ in range(rows * cols)]

    @classmethod
    def identity(cls, n, dtype=float):
        i = Matrix([dtype(0)] * (n * n), n, n)
        i[0: n*n: n+1] = [dtype(1)] * n

        return i

    @property
    def shape(self):
        return self._shape

    @property
    def size(self):
        return len(self._data)

    def _init_from_other_matrix(self, other):
        self._data = other[0:]
        self._shape = other.shape

    def _init_from_list_of_lists(self, data, dtype):
        rows = len(data)
        if rows == 0:
            raise ValueError('Initialization data has invalid shape: {} rows'.format(rows))

        cols = {len(r) if hasattr(r, '__len__') else 1 for r in data}
        if len(cols) > 1:
            raise ValueError('Initialization data has inconsistent shapes: {} rows {} columns'.format(rows, cols))

        cols = cols.pop()
        if cols == 0:
            raise ValueError('Initialization data has invalid shape: {} rows {} columns'.format(rows, cols))

        self._data = [dtype(data[r][c]) for r in range(rows) for c in range(cols)]
        self._shape = MatrixShape(rows, cols)

    def _init_from_single_list(self, data, rows, cols, dtype):
        self._shape = MatrixShape(rows, cols)
        if len(data) != rows * cols:
            raise ValueError('invalid initialization data length: expected {}*{} entries got {}'.format(rows, cols, rows * cols))

        self._data = [dtype(data[r * cols + c]) for r in range(rows) for c in range(cols)]

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._data[item]
        elif isinstance(item, tuple) and len(item) == 2:
            r, c = item
            if r >= self.shape.rows:
                raise IndexError('row index out of range')
            if c >= self.shape.columns:
                raise IndexError('column index out of range')

            return self._data[r * self.shape.columns + c]
        elif isinstance(item, int):
            if item >= self.shape.rows:
                raise IndexError('row index out of range')

            return self._data[item * self.shape.columns: (item + 1) * self.shape.columns]

    def __setitem__(self, item, val):
        if isinstance(item, int) and len(val) == self.shape.columns:
            if item >= self.shape.rows:
                raise IndexError('row index out of range')

            start = item * self.shape.columns
            end = start + self.shape.columns
            self._data[start:end] = map(self.dtype, val)
            return
        elif isinstance(item, tuple) and len(item) == 2:
            r, c = item
            if r >= self.shape.rows:
                raise IndexError('row index out of range')
            if c >= self.shape.columns:
                raise IndexError('column index out of range')

            self._data[r * self._shape.columns + c] = self.dtype(val)
        elif isinstance(item, slice):
            self._data[item] = val

    def __str__(self):
        rows, cols = self.shape
        if rows == 0:
            return '[]\n'
        res = ''
        for r in range(rows):
            if r == 0:
                res += f'[{self[r]}'
            elif r < rows:
                res += f' {self[r]}'
            if r == rows - 1:
                res += ']'
            else:
                res += '\n'

        return res

    def __repr__(self):
        rows, cols = self.shape
        if rows == 0:
            return 'Matrix([])\n'
        res = ''
        for r in range(rows):
            if r == 0:
                res += f'Matrix([{self[r]}'
            elif r < rows:
                res += f'        {self[r]}'
            if r == rows - 1:
                res += '])'
            else:
                res += ',\n'

        return res

    def __len__(self):
        """Get number of elements in matrix (rows*columns)"""
        return len(self._data)

    @property
    def T(self):
        """Get the transpose of this matrix

        :return: matrix transpose
        """
        cols = self.shape.columns
        end = len(self._data)
        mt = [self[c: end: cols] for c in range(cols)]

        return Matrix(mt)

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('Matrix not comparable with {}'.format(type(other)))
        return self.shape == other.shape and self._data == other._data

    def __add__(self, other):
        _check_operand_types(self, other, '+')
        _check_equal_shape(self, other)
        rows, cols = self._shape

        return Matrix([self[r, c] + other[r, c] for r in range(rows) for c in range(cols)], *self._shape)

    def __sub__(self, other):
        _check_operand_types(self, other, '-')
        _check_equal_shape(self, other)
        rows, cols = self._shape

        return Matrix([self[r, c] - other[r, c] for r in range(rows) for c in range(cols)], *self._shape)

    @staticmethod
    def _matmul(lhs, rhs):
        _check_equal_inner_dimensions(lhs, rhs)
        rows, cols = lhs.shape.rows, rhs.shape.columns

        m = Matrix(rows, cols)
        inner = lhs.shape.columns
        for r in range(rows):
            for c in range(cols):
                m[r, c] = sum([lhs[r, i] * rhs[i, c] for i in range(inner)])

        return m

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self._matmul(self, other)

        rows, cols = self._shape

        m = [self[r, c] * other for r in range(rows) for c in range(cols)]

        return Matrix(m, rows, cols)

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            return self._matmul(other, self)

        rows, cols = self._shape
        m = [self[r, c] * other for r in range(rows) for c in range(cols)]

        return Matrix(m, rows, cols)

    def __matmul__(self, other):
        return self._matmul(self, other)

    def __rmatmul__(self, other):
        return self._matmul(other, self)

    def row(self, row):
        """Retrieve an entire row

       :param row: row number to retrieve
       :return: row data
       """
        return self[row]

    def column(self, col):
        """Retrieve an entire column

        :param col: column to retrieve
        :return: column data
        """
        return self[col: len(self): self.shape.columns]

    def exchange_rows(self, r, s):
        """Perform a row exchange of rows r and s.
        Get a new Matrix, leaving the original unchanged.

        :param r: first row
        :param s: second row
        :return:  Matrix copy with rows r and s exchanged
        """
        rows, cols = self.shape
        if r >= rows or s >= rows:
            raise IndexError('row index out of range')

        m = Matrix(self)
        m[r], m[s] = m[s], m[r]

        return m
