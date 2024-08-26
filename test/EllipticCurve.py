from Point import Point
from tools import *

class EllipticCurve:
    '''Clase que crea una curva elíptica usando un campo finito modulo p > 3'''

    # Punto al infinito siempre será None. Ignorar esta prueba unitaria
    inf_p = Point.infinite_point

    def __init__(self, prime=3, a=1, b=1):
        '''Construimos la curva elíptica a partir de los parámetros a, b modulo p'''
        self.prime = prime
        self.a = a
        self.b = b
        self.points = self.get_points()

    def __str__(self):
        '''La curva debe ser representada como: y^2 = x^3 + ax + b mod p'''
        return f"y^2 = x^3 + {self.a}x + {self.b} mod {self.prime}"

    def isInCurve(self, point):
        '''Nos dice si un punto "point" pertenece a esta curva'''
        if point == self.inf_p or point is None:
            return True
        if not isinstance(point, Point):
            return False  # Return False instead of raising an exception
        x, y = point.x, point.y
        return (y**2 - (x**3 + self.a * x + self.b)) % self.prime == 0

    def get_points(self):
        '''Nos da todos los puntos que pertenecen a la curva elíptica'''
        points = []
        for x in range(self.prime):
            for y in range(self.prime):
                point = Point(x, y)
                if self.isInCurve(point):
                    points.append(point)
        points.append(self.inf_p)  # Add the point at infinity
        return points

    def sum(self, p, q):
        '''Suma p + q regresando un nuevo punto modulo prime
        como está definido en las curvas elípticas. Recuerda que el punto al
        infinito funciona como neutro aditivo'''
        if p == self.inf_p:
            return q
        if q == self.inf_p:
            return p

        if not (self.isInCurve(p) and self.isInCurve(q)):
            raise ValueError("Both points must lie on the curve")

        x1, y1 = p.x, p.y
        x2, y2 = q.x, q.y

        if p == q:
            denom = inv_mult(2 * y1, self.prime)
            if denom is None:  # Handle case where the inverse does not exist
                return self.inf_p
            m = (3 * x1**2 + self.a) * denom % self.prime
        else:
            if x1 == x2:
                return self.inf_p
            denom = inv_mult(x2 - x1, self.prime)
            if denom is None:
                return self.inf_p
            m = (y2 - y1) * denom % self.prime

        x3 = (m**2 - x1 - x2) % self.prime
        y3 = (m * (x1 - x3) - y1) % self.prime

        return Point(x3, y3)

    def mult(self, k, p):
        '''Suma k veces el punto p (o k(P)).
        Si k < 0 entonces se suma el inverso de P k veces'''
        if k == 0 or p == self.inf_p:
            return self.inf_p
        if k < 0:
            return self.mult(-k, self.inv(p))

        result = self.inf_p
        addend = p

        while k:
            if k & 1:
                result = self.sum(result, addend)
            addend = self.sum(addend, addend)
            k >>= 1

        return result

    def order(self, p):
        if p == self.inf_p:
            return 1
        if not self.isInCurve(p):
            raise ValueError("Point is not on the curve")
        
        k = 1
        current = p
        while current != self.inf_p:
            current = self.sum(current, p)
            k += 1
            if k > len(self.points):
                return None  # Point doesn't have a finite order
        return k

    def cofactor(self, p):
        if not self.isInCurve(p):
            raise ValueError("Point is not on the curve")
        order_p = self.order(p)
        if order_p is None:
            return None
        return len(self.points) // order_p


    def inv(self, p):
        '''Regresa el inverso aditivo de este punto. Recuerda que es el mismo punto reflejado
        en el eje x'''
        if p == self.inf_p:
            return self.inf_p
        if not isinstance(p, Point):
            raise TypeError("Expected a Point object")
        return Point(p.x, -p.y % self.prime)
