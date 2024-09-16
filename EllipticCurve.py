from Point import Point

def inv_mult(a, p):
    '''Calculates the modular inverse of a modulo p.'''
    a = a % p
    if a == 0:
        raise ValueError("No inverse exists")
    return pow(a, -1, p)

class EllipticCurve:
    '''Class that creates an elliptic curve over a finite field modulo p > 2'''

    # The point at infinity is represented by None
    inf_p = None

    def __init__(self, prime=3, a=1, b=1):
        if prime <= 2:
            raise ValueError("The value of p must be greater than 2.")
        self.p = prime
        self.a0 = a
        self.b0 = b
        self.a = a % prime
        self.b = b % prime
        discriminant = (4 * self.a**3 + 27 * self.b**2) % prime
        if discriminant == 0:
            raise ValueError("Invalid elliptic curve. The discriminant cannot be 0.")
        self.prime = prime  # Retain the original 'prime' attribute for tests
        self.points = self.get_points()  # Store all points on the curve

    def __str__(self):
        '''Represents the curve as: y^2 = x^3 + ax + b mod p'''
        return f"y^2 = x^3 + {self.a0}x + {self.b0} mod {self.p}"

    def isInCurve(self, point):
        '''Checks if a point belongs to this curve'''
        if point == self.inf_p:
            return True
        if not isinstance(point, Point):
            return False
        lhs = (point.y ** 2) % self.p
        rhs = (point.x ** 3 + self.a * point.x + self.b) % self.p
        return lhs == rhs

    def get_points(self):
        '''Returns all points that belong to the elliptic curve'''
        points = [self.inf_p]  # Start with the point at infinity
        for x in range(self.p):
            for y in range(self.p):
                point = Point(x, y)
                if self.isInCurve(point):
                    points.append(point)
        return points

    def sum(self, p, q):
        '''Adds p + q, returning a new point modulo prime'''
        if p == self.inf_p:
            return q
        if q == self.inf_p:
            return p
        if p.x == q.x and (p.y + q.y) % self.p == 0:
            return self.inf_p
        if p == q:
            # Tangent case, p == q
            if p.y == 0:
                return self.inf_p  # Point at infinity
            numerator = (3 * p.x**2 + self.a) % self.p
            denominator_inv = inv_mult((2 * p.y) % self.p, self.p)
            m = (numerator * denominator_inv) % self.p
        else:
            # Normal case p != q
            numerator = (q.y - p.y) % self.p
            denominator_inv = inv_mult((q.x - p.x) % self.p, self.p)
            m = (numerator * denominator_inv) % self.p
        x_r = (m**2 - p.x - q.x) % self.p
        y_r = (m * (p.x - x_r) - p.y) % self.p
        return Point(x_r, y_r)

    def mult(self, k, p):
        '''Adds the point p to itself k times (i.e., computes k * P).'''
        result = self.inf_p
        addend = p

        if k == 0:
            return self.inf_p

        if k < 0:
            k = -k
            addend = self.inv(p)

        while k:
            if k & 1:
                result = self.sum(result, addend)
            addend = self.sum(addend, addend)
            k >>= 1

        return result

    def order(self, p):
        '''Returns the smallest integer k such that k * P = point at infinity.'''
        if not self.isInCurve(p):
            raise ValueError("Point does not belong to the curve.")
        k = 1
        current_point = p
        while current_point != self.inf_p:
            current_point = self.sum(current_point, p)
            k += 1
        return k

    def cofactor(self, p):
        '''Returns the total number of points on the curve divided by the order of the point.'''
        total_points = len(self.points)
        point_order = self.order(p)
        return total_points // point_order

    def inv(self, p):
        '''Returns the additive inverse of this point.'''
        if p == self.inf_p:
            return self.inf_p
        return Point(p.x, (-p.y) % self.p)
