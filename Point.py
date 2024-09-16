class Point:
    '''Class that represents a point in a 2D plane'''

    # Point at infinity (we will use None to indicate the point at infinity)
    infinite_point = None

    def __init__(self, x=0, y=0):
        '''Constructor: Constructs a point in a 2D plane with coordinates (x, y)'''
        self.x = x
        self.y = y

    def __str__(self):
        '''String representation. Use str(p)'''
        if self == Point.infinite_point:
            return "Point at infinity"
        return f"({self.x}, {self.y})"

    def __repr__(self):
        '''String representation for print(p)'''
        return self.__str__()

    def __eq__(self, other):
        '''Comparison between two points. Use =='''
        if other is None:
            return False
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        '''Makes Point instances hashable'''
        return hash((self.x, self.y))

    def set(self, x, y):
        '''Rewrites the values of x and y for this point.'''
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Coordinates must be numbers.")
        self.x = x
        self.y = y
