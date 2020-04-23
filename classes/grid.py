class Grid:
    rows = 0
    cols = 0
    tiles = []
    elements = []

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tiles = [[0 for x in range(rows)] for y in range(rows)]
