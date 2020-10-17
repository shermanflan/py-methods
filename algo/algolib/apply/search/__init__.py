from collections import defaultdict
from enum import Enum, auto


class Color(Enum):
    """
    White: Vertex has not been visited.
    Gray: Vertex has been visited, but adjacent vertices have not.
    Black: Vertex and its adjacent vertices have been visited.
    """
    WHITE = auto()
    GRAY = auto()
    BLACK = auto()


