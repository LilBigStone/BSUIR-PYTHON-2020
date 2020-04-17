from cmath import sqrt


class Vector:

    def __init__(self, size, *values):
        self._dimension = size
        self._vector = self.validate_input(list(values)) or [0] * size

    def validate_input(self, values):
        if values:
            for val in values:
                if not isinstance(val, (int, float)):
                    raise ValueError('Components of the vector must be the numbers (integer or float).')
            if len(values) > self._dimension:
                while len(values) != self._dimension:
                    values.pop()
            elif len(values) < self._dimension:
                difference = self._dimension - len(values)
                values.extend([0.0] * difference)
        return values

    def __str__(self):
        return f'<{str(self._vector)[1:-1]}>'

    def __repr__(self):
        return f'<{str(self._vector)[1:-1]}>'

    def __len__(self):
        return self._dimension

    def __getitem__(self, index):
        if index < -len(self) or index >= len(self):
            raise IndexError(f'Vector index [{index}] out of range.')
        return self._vector[index]

    def __setitem__(self, index, value):
        if index < -len(self) or index >= len(self):
            raise IndexError(f'Vector index [{index}] out of range.')
        if not isinstance(value, (int, float)):
            raise ValueError('Components of the vector must be the numbers (integer or float).')
        self._vector[index] = value

    def __neg__(self):
        return Vector(self._dimension, *[-val for val in self])

    def __add__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError('Vectors must have the same dimensions to perform an operation')
            return Vector(len(self), *[self[i] + other[i] for i in range(len(self))])
        elif isinstance(other, (int, float)):
            return Vector(len(self), *[val + other for val in self])
        else:
            raise ValueError('Operation supports the following input: Vector object or number (integer or float)')

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self + (-other)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self._vector == other._vector
        else:
            return False

    def __mul__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError('Vectors must have the same dimensions to perform an operation')
            return sum(Vector(len(self), *[self[i] * other[i] for i in range(len(self))]))
        elif isinstance(other, (int, float)):
            return Vector(len(self), *[val * other for val in self])
        else:
            raise ValueError('Operation supports the following input: Vector object or number (integer or float)')

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other
