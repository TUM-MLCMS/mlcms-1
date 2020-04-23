import tkinter as tk
from classes.pedestrian import Pedestrian
from classes.obstacle import Obstacle
from classes.target import Target
from classes.grid import Grid

class CMS(tk.Canvas):
    def __init__(self):

        self.offset = 5
        
        self.width = 600
        self.height = 600

        super().__init__(width=self.width,
                         height=self.height,
                         background="black",
                         highlightthickness=0)
        
        self.grid = Grid(5, 5)
        self.cell_size = 100

        self.grid_elements = [Pedestrian((0,0)), Obstacle((1,0)), Target((2,0)), Pedestrian((3,0)), Obstacle((4,0)), Obstacle((4,4))]

        self.rect_start_x = self.width // 2 - self.grid.cols / 2 * (self.cell_size) - (self.grid.cols + 1) / 2 * (self.offset)
        self.rect_start_y = self.height // 2 - self.grid.rows / 2 * (self.cell_size) - (self.grid.rows + 1) / 2 * (self.offset)
        self.rect_end_x = self.width // 2 + self.grid.cols / 2 * (self.cell_size) + (self.grid.cols + 1) / 2 * (self.offset)
        self.rect_end_y = self.height // 2 + self.grid.rows / 2 * (self.cell_size) + (self.grid.rows + 1) / 2 * (self.offset)

        self.create()

    def create(self):
        self.create_rectangle(
            self.rect_start_x,
            self.rect_start_y,
            self.rect_end_x,
            self.rect_end_y,
            outline="#FFFFFF"
        )

        for element in self.grid_elements:
            coord_x, coord_y = self.coordinate(*element.start_pos)
            self.fill(coord_x, coord_y, element.color)

    def coordinate(self, x, y):
        return self.rect_start_x + x * (self.cell_size) + (x + 1) * self.offset, self.rect_start_y + y * (self.cell_size) + (y + 1) * self.offset

    def fill(self, x, y, color):
        self.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill=color)