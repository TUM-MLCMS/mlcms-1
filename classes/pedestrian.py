import math

class Pedestrian:

    max_speed = 0 # Maximum allowed speed for pedestrians.

    def __init__(self, start_pos):
        self.tag = 'P'
        self.color = "#009900"
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.has_arrived = False
        self.total_distance_moved = 0
        self.steps_moved = 0
        self.steps_total = 0
        self.max_speed = 0
        self.age = -1

    # Moves the pedestrian to the desired direction.
    def move(self, target):
        self.steps_total += 1
        if (self.get_speed() <= self.max_speed) or (self.max_speed == 0):
            if not self.has_arrived:
                self.total_distance_moved = self.total_distance_moved + 0.4*math.sqrt(pow(target[0] - self.current_pos[0], 2) + pow(target[1] - self.current_pos[1], 2))
                self.steps_moved = self.steps_moved + 1
                self.current_pos = (target[0], target[1])
                return True
        return False

    # Each cell is 40 centimeters long, and each step takes 3.325 seconds in real life.
    def get_speed(self):
        if self.steps_moved == 0:
            return 0
        else:
            return self.total_distance_moved/(self.steps_total/3.325)


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
