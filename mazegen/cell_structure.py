class WallEdge():
    """Represents a single wall segment shared by up to two Cells."""
    def __init__(self, is_open: bool = False) -> None:
        """
        Initialization of the WallEdge class.

        Parameters:
            is_open (bool): True if the wall is open,
                False if closed. Defaults to False.
        """
        self.is_open = is_open


class Cell():
    """Represents a position in the maze surrounded by four WallEdges."""
    def __init__(self, x: int, y: int,
                 north: WallEdge, east: WallEdge,
                 south: WallEdge, west: WallEdge) -> None:
        """
        Initialization of the Cell class.

        Parameters:
            x (int): coordinate for the X axis from 0 to width.
            y (int): coordinate for the Y axis from 0 to height.
            north (WallEdge): wall shared with cell (x, y-1).
            east (WallEdge): wall shared with cell (x+1, y).
            south (WallEdge): wall shared with cell (x, y+1).
            west (WallEdge): wall shared with cell (x-1, y).

        """
        self.x = x
        self.y = y
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.blocked = False
        self.visited = False
