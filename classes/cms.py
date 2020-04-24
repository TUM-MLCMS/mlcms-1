import tkinter as tk
from classes.pedestrian import Pedestrian
from classes.obstacle import Obstacle
from classes.target import Target
from classes.grid import Grid
import math


# Main class of the CMS
class CMS(tk.Canvas):
    def __init__(self):
        self.offset = 5

        self.width = 600
        self.height = 600

        self.success = False
        self.status = []

        super().__init__(width=self.width,
                         height=self.height,
                         background="black",
                         highlightthickness=0)

        self.grid = Grid(10, 10)
        self.cell_size = 50

        self.grid_elements = {
            'P': [Pedestrian((0, 8)), Pedestrian((1, 2)), Pedestrian((3, 5)), Pedestrian((8, 8))],
            'T': Target((9, 4)),
            'O': []
        }

        self.rect_start_x = self.width // 2 - self.grid.cols / 2 * self.cell_size - (self.grid.cols + 1) / 2 * (
            self.offset)
        self.rect_start_y = self.height // 2 - self.grid.rows / 2 * self.cell_size - (self.grid.rows + 1) / 2 * (
            self.offset)
        self.rect_end_x = self.width // 2 + self.grid.cols / 2 * self.cell_size + (self.grid.cols + 1) / 2 * (
            self.offset)
        self.rect_end_y = self.height // 2 + self.grid.rows / 2 * self.cell_size + (self.grid.rows + 1) / 2 * (
            self.offset)

        self.loop()

    # Loop.
    def loop(self):
        self.draw()
        self.after(500, self.loop)

    # Draws the canvas.
    def draw(self):
        self.delete("all")

        self.create_rectangle(
            self.rect_start_x,
            self.rect_start_y,
            self.rect_end_x,
            self.rect_end_y,
            outline="#FFFFFF"
        )

        self.evaluate()

    # Returns the respective coordinates.
    def coordinate(self, x, y):
        return self.rect_start_x + x * self.cell_size + (x + 1) * self.offset, self.rect_start_y + y * (
            self.cell_size) + (y + 1) * self.offset

    # Fills the cells.
    def fill(self, x, y, color):
        self.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill=color)

    # Evaluates the next state of the system.
    def evaluate(self):
        if len(self.status) == 0:
            for i in range(0, len(self.grid_elements['P'])):
                self.status.append(False)

        # Rendering Obstacles.
        for obstacle in self.grid_elements['O']:
            coord_x, coord_y = self.coordinate(*obstacle.current_pos)
            self.fill(coord_x, coord_y, obstacle.color)

        # Rendering Target.
        coord_x, coord_y = self.coordinate(*self.grid_elements['T'].current_pos)
        self.fill(coord_x, coord_y, self.grid_elements['T'].color)

        # Rendering Pedestrians.
        for i, pedestrian in enumerate(self.grid_elements['P']):
            direction = self.utility(pedestrian)
            if not self.success:
                self.success = True
                for s in self.status:
                    if not s:
                        self.success = False
                pedestrian.move(direction)

            coord_x, coord_y = self.coordinate(*pedestrian.current_pos)
            self.fill(coord_x, coord_y, pedestrian.color)
            if direction == 'SUCCESS':
                self.status[i] = True

    # Utility function, calculates the distance to the target and returns the direction maximizing utility.
    def utility(self, pedestrian):
        right = math.sqrt(pow(self.grid_elements['T'].current_pos[0] - (pedestrian.current_pos[0] + 1), 2) +
                          pow(self.grid_elements['T'].current_pos[1] - pedestrian.current_pos[1], 2))

        left = math.sqrt(pow(self.grid_elements['T'].current_pos[0] - (pedestrian.current_pos[0] - 1), 2) +
                         pow(self.grid_elements['T'].current_pos[1] - pedestrian.current_pos[1], 2))

        up = math.sqrt(pow(self.grid_elements['T'].current_pos[0] - pedestrian.current_pos[0], 2) +
                       pow(self.grid_elements['T'].current_pos[1] - (pedestrian.current_pos[1] + 1), 2))

        down = math.sqrt(pow(self.grid_elements['T'].current_pos[0] - pedestrian.current_pos[0], 2) +
                         pow(self.grid_elements['T'].current_pos[1] - (pedestrian.current_pos[1] - 1), 2))

        u = [right, left, up, down]

        for move in u:
            if move == 0:
                return 'SUCCESS'

        index = u.index(min(u))

        if index == 0:
            return 'R'

        elif index == 1:
            return 'L'

        elif index == 2:
            return 'U'

        elif index == 3:
            return 'D'

        else:
            return 'ERROR'
