
class Vector(list):

    def __init__(self, elements):
        super().__init__(elements)

    @property
    def dimensions(self):
        return len(self),

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vector([a + other for a in self])
        elif not isinstance(other, Vector):
            raise TypeError('vector can only be added to a number (float or int), or another vector')

        if self.dimensions != other.dimensions:
            raise ValueError('can not add vectors of different dimensions')

        element_sums = [a + b for a, b in zip(self, other)]

        return Vector(element_sums)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError('vector can only be multiplied by a number (float or int)')
        element_prods = [other * e for e in self]

        return Vector(element_prods)

    def __rmul__(self, other):
        return self * other

    def dot(self, other):
        return sum([a * b for a, b in zip(self, other)])
