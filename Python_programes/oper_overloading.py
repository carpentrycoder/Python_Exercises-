class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Overloading the addition operator '+'
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Unsupported operand type")

    # Overloading the equality operator '=='
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False

    # Overloading the string representation
    def __str__(self):
        return f"Point({self.x}, {self.y})"

# Creating instances of the Point class
point1 = Point(1, 2)
point2 = Point(3, 4)

# Using overloaded operators
result = point1 + point2
print(result)  # Outputs: Point(4, 6)

equality_check = point1 == point2
print(equality_check)  # Outputs: False