import tkinter as tk
from classes.pedestrian import Pedestrian
from classes.obstacle import Obstacle
from classes.target import Target


class CMS(tk.Canvas):
    def __init__(self):

        self.red = "#CC0000"
        self.purple = "#9900CC"
        self.green = "#009900"
        self.white = "#FFFFFF"

        self.p = Pedestrian
        self.o = Obstacle
        self.t = Target

        self.offset = 5

        self.width = 800
        self.height = 600

        super().__init__(width=self.width,
                         height=self.height,
                         background="black",
                         highlightthickness=0)

        self.margin = {'right': 150, 'left': 150, 'top': 50, 'bottom': 50}

        self.cell_size = 100
        self.positions = [self.coordinate(*self.p.start),
                          self.coordinate(*self.o.start),
                          self.coordinate(*self.t.start)]

        self.create()

    def create(self):

        self.create_text(400,
                         25,
                         text=f"Machine Learning in Crowd Modelling & Simulation",
                         fill="#FFF",
                         font=("TkDefaultFont", 15))

        self.create_rectangle(
            self.margin['left'] - self.offset,
            self.margin['bottom'] - self.offset,
            self.width - self.margin['right'] + self.offset,
            self.height - self.margin['top'] + self.offset,
            outline=self.white
        )

        for i, (x, y) in enumerate(self.positions):
            if i == 0:
                self.fill(x, y, self.green)
            if i == 1:
                self.fill(x, y, self.red)
            if i == 2:
                self.fill(x, y, self.purple)

    def coordinate(self, x, y):
        return self.cell_size * x + self.margin['left'], self.cell_size * y + self.margin['bottom']

    def fill(self, x, y, color):
        offset = self.offset
        self.create_rectangle(x + offset, y + offset, x + self.cell_size - offset, y + self.cell_size - offset,
                              fill=color)
