class Pedestrian:
    def __init__(self, start_pos):
        self.tag = 'P'
        self.color = "#009900"
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.has_arrived = False

    # Moves the pedestrian to the desired direction.
    def move(self, target):
        if not self.has_arrived:
            self.current_pos = (target[0], target[1])

    # Gets all valid neighbors of the pedestrian.
    def get_all_neighbors(self, grid_rows, grid_cols):
        neighbors = []

        self_col, self_row = self.current_pos
        start_col = max(0, self_col - 1)
        start_row = max(0, self_row - 1)

        end_col = min(self_col + 1, grid_cols - 1)
        end_row = min(self_row + 1, grid_rows - 1)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                neighbors.append((col, row))

        return neighbors
