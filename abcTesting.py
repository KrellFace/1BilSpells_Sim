from abc import ABC, abstractmethod
from enum import Enum

# Step 1: Define an Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Step 2: Define an Abstract Base Class
class Shape(ABC):
    
    @property
    @abstractmethod
    def color(self) -> Color:
        """This property must be of type Color."""
        pass

    @color.setter
    @abstractmethod
    def color(self, value: Color):
        """Setter for the color property."""
        pass

# Step 3: Implement a Concrete Class
class Circle(Shape):
    
    def __init__(self, color: Color):
        self._color = color
    
    @property
    def color(self) -> Color:
        return self._color
    
    @color.setter
    def color(self, value: Color):
        if not isinstance(value, Color):
            raise ValueError("Color must be an instance of the Color Enum")
        self._color = value

# Usage
circle = Circle(Color.RED)
print(circle.color)  # Output: Color.RED
circle.color = Color.GREEN  # Works fine