import tkinter as tk
from classes.pedestrian import Pedestrian
from classes.obstacle import Obstacle
from classes.target import Target
from classes.grid import Grid
import math


# Main class of the CMS
class CMS(tk.Canvas):
    def __init__(self):
        self.is_running = False
        self.offset = 5
        self.step = 0

        self.width = 600
        self.height = 600

        self.success = False

        super().__init__(width=self.width,
                         height=self.height,
                         background="black",
                         highlightthickness=0)

        self.simulation_grid = Grid(0, 0)
        self.simulation_grid.read_from_file("grid_file.in")
        self.simulation_grid.create_distance_field()

        self.cell_size = min(self.width, self.height) / max(self.simulation_grid.rows, self.simulation_grid.cols) - self.offset * 2

        self.rect_start_x = self.width // 2 - self.simulation_grid.cols / 2 * self.cell_size - (self.simulation_grid.cols + 1) / 2 * (
            self.offset)
        self.rect_start_y = self.height // 2 - self.simulation_grid.rows / 2 * self.cell_size - (self.simulation_grid.rows + 1) / 2 * (
            self.offset)
        self.rect_end_x = self.width // 2 + self.simulation_grid.cols / 2 * self.cell_size + (self.simulation_grid.cols + 1) / 2 * (
            self.offset)
        self.rect_end_y = self.height // 2 + self.simulation_grid.rows / 2 * self.cell_size + (self.simulation_grid.rows + 1) / 2 * (
            self.offset)

    #Start or stop the simulation
    def start_or_stop(self):
        self.is_running = not self.is_running
        self.loop()
    
    #Get simulation step text object from the GUI
    def set_step_text(self, current_step_text):
        self.current_step_text = current_step_text

    # Loop.
    def loop(self):
        if self.is_running:
            self.step = self.step + 1
            self.current_step_text.set(f"Current Step: {self.step}")
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
        # Rendering Obstacles.
        for obstacle in self.simulation_grid.elements['O']:
            coord_x, coord_y = self.coordinate(*obstacle.current_pos)
            self.fill(coord_x, coord_y, obstacle.color)

        #Check success condition
        self.success = True
        for pedestrian in self.simulation_grid.elements['P']:
            if not pedestrian.has_arrived:
                self.success = False
                break

        # Rendering Pedestrians.
        for pedestrian in self.simulation_grid.elements['P']:
            if not pedestrian.has_arrived:
                distance, move_target = self.get_move_coordinate(pedestrian)
                pedestrian.move(move_target)
                if distance == 0:
                    pedestrian.has_arrived = True

            coord_x, coord_y = self.coordinate(*pedestrian.current_pos)
            self.fill(coord_x, coord_y, pedestrian.color)       

        # Rendering Target.
        coord_x, coord_y = self.coordinate(*self.simulation_grid.elements['T'].current_pos)
        self.fill(coord_x, coord_y, self.simulation_grid.elements['T'].color)
 

    # Utility function, calculates the distance to the target and returns the direction maximizing utility.
    def get_move_coordinate(self, pedestrian):
        neighbors = pedestrian.get_all_neighbors(self.simulation_grid.rows, self.simulation_grid.cols)

        current_selected_neighbor = {}
        current_min_distance = float("inf")
        
        for neighbor in neighbors:
            col, row = neighbor
            distance = self.simulation_grid.distance_field[row][col]
            if distance < current_min_distance:
                current_min_distance = distance
                current_selected_neighbor = neighbor
    
        return current_min_distance, current_selected_neighbor
