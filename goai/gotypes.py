import enum
from collections import namedtuple

# switching player turns
class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

# represent coordinates on the board

# namedtuple lets us access the coordinates as point.row and point.col instead of point[0] and point[1]

class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]
    
    def __deepcopy__(self, memodict={}):
        return self