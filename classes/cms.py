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
        self.is_finished = False
        self.offset = {'V': 20, 'H': 20, 'D': 2}  # Vertical & Horizontal gap of the canvas, offset for drawing objects.
        self.step = 0
        self.current_step_text = None
        self.control_button = None
        self.utility = []  # Utility matrix that takes into account also the positions of the pedestrians.
        self.current_pedestrian = -1
        self.not_arrived = [-1]
        self.arrived = {'last_index': -1, 'flag': False}

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

        self.cell_size = min(self.width - self.offset['H'] * 2, self.height - self.offset['V'] * 2) / max(
            self.simulation_grid.rows,
            self.simulation_grid.cols)

        # New offset values set to center the simulation.
        self.offset['V'] = (self.height - self.simulation_grid.rows * self.cell_size) / 2
        self.offset['H'] = (self.width - self.simulation_grid.cols * self.cell_size) / 2

        self.rect_start_x = self.offset['H']
        self.rect_start_y = self.offset['V']
        self.rect_end_x = self.width - self.offset['H']
        self.rect_end_y = self.height - self.offset['V']

        for i in range(0, len(self.simulation_grid.elements['P'])):
            self.not_arrived.append(i)

    # Start or stop the simulation
    def start_or_stop(self, button):
        self.is_running = not self.is_running
        self.control_button = button
        self.loop()

    # Start or stop the simulation
    def reset(self, text, button):
        self.control_button = button
        self.is_running = False
        self.is_finished = False
        self.step = 0
        self.success = False
        self.utility = []
        self.current_pedestrian = -1
        self.not_arrived = [-1]
        self.arrived = {'last_index': -1, 'flag': False}

        self.simulation_grid = Grid(0, 0)
        self.simulation_grid.read_from_file("grid_file.in")
        self.simulation_grid.create_distance_field()

        for i in range(0, len(self.simulation_grid.elements['P'])):
            self.not_arrived.append(i)

        self.is_running = True
        self.set_step_text(text)
        self.loop()

    # Get simulation step text object from the GUI
    def set_step_text(self, current_step_text):
        self.current_step_text = current_step_text

    # Loop.
    def loop(self):
        if self.is_running:
            self.step = self.step + 1
            self.current_step_text.set(f"Current Step: {self.step}")
            self.draw()
            self.after(100, self.loop)

    # Draws the canvas.
    def draw(self):
        self.delete("all")

        # Draw the borders.
        self.create_rectangle(
            self.rect_start_x - self.offset['D'] * 2,
            self.rect_start_y - self.offset['D'] * 2,
            self.rect_end_x + self.offset['D'] * 2,
            self.rect_end_y + self.offset['D'] * 2,
            outline="#FFFFFF"
        )

        # Update the index of the current pedestrian.
        if len(self.not_arrived) != 1:
            if self.arrived['flag']:
                if self.arrived['last_index'] != len(self.not_arrived):
                    self.current_pedestrian = self.not_arrived[self.arrived['last_index']]
                    self.arrived = {'last_index': -1, 'flag': False}
                else:
                    self.current_pedestrian = self.not_arrived[1]
                    self.arrived = {'last_index': -1, 'flag': False}

            else:
                for i in range(0, len(self.not_arrived)):
                    if self.not_arrived[i] == self.current_pedestrian:
                        if i == len(self.not_arrived) - 1:
                            self.current_pedestrian = self.not_arrived[1]
                        else:
                            self.current_pedestrian = self.not_arrived[i + 1]
                        break

        # Call the evaluation, which moves and renders the current state.
        self.evaluate(self.current_pedestrian)

        # Print coordinates of cells. For development.
        for i in range(0, self.simulation_grid.rows):
            for j in range(0, self.simulation_grid.cols):
                x, y = self.coordinate(i, j)

                self.create_text(x + self.offset['D'] + self.cell_size / 2,
                                 y + self.offset['D'] + self.cell_size / 1.3,
                                 fill="#FFFFFF",
                                 text="(" + str(i) + "," + str(j) + ")")

    # Returns the respective coordinates.
    def coordinate(self, x, y):
        return self.rect_start_x + x * self.cell_size, self.rect_start_y + y * self.cell_size

    # Fills the cells.
    def fill(self, x, y, color, i):
        self.create_rectangle(x + self.offset['D'],
                              y + self.offset['D'],
                              x + self.cell_size - self.offset['D'],
                              y + self.cell_size - self.offset['D'],
                              fill=color)
        self.create_text(x + self.offset['D'] + self.cell_size / 2,
                         y + self.offset['D'] + self.cell_size / 2,
                         fill="#FFFFFF",
                         text=i)

    # Evaluates the next state of the system.
    def evaluate(self, current):
        # Rendering Obstacles.
        for obstacle in self.simulation_grid.elements['O']:
            coord_x, coord_y = self.coordinate(*obstacle.current_pos)
            self.fill(coord_x, coord_y, obstacle.color, "O")

        # Rendering Pedestrians.
        for i, pedestrian in enumerate(self.simulation_grid.elements['P']):
            coord_x, coord_y = self.coordinate(*pedestrian.current_pos)
            self.fill(coord_x, coord_y, pedestrian.color, str(i + 1))

        # Rendering Target.
        coord_x, coord_y = self.coordinate(*self.simulation_grid.elements['T'].current_pos)
        self.fill(coord_x, coord_y, self.simulation_grid.elements['T'].color, "T")

        # Check success condition
        self.success = True
        for pedestrian in self.simulation_grid.elements['P']:
            if not pedestrian.has_arrived:
                self.success = False
                break

        # Get the current pedestrian.
        pedestrian = self.simulation_grid.elements['P'][current]

        # Move the current pedestrian.
        if not pedestrian.has_arrived:
            distance, move_target = self.get_move_coordinate(pedestrian)
            pedestrian.move(move_target)
            if distance == 0:
                pedestrian.has_arrived = True
                self.arrived['flag'] = True
                self.arrived['last_index'] = self.not_arrived.index(self.current_pedestrian)
                self.not_arrived.remove(current)

        # Render the current pedestrians next move with red. For tracking.
        coord_x, coord_y = self.coordinate(*pedestrian.current_pos)
        self.fill(coord_x, coord_y, "#CC0000", str(current + 1))

        # Check if the simulation reached the desired state.
        if self.success:
            self.is_finished = True
            self.control_button.set("Restart")
            self.start_or_stop(self.control_button)

    # Utility function, calculates the distance to the target and returns the direction maximizing utility.
    def get_move_coordinate(self, pedestrian):
        neighbors = pedestrian.get_all_neighbors(self.simulation_grid.rows, self.simulation_grid.cols)

        current_selected_neighbor = {}
        current_min_distance = float("inf")

        for d in self.simulation_grid.distance_field:
            self.utility.append(d[:])

        for i in self.simulation_grid.elements['P']:
            for j in neighbors:
                if i.current_pos == j:
                    if not i.has_arrived:
                        if i.current_pos != pedestrian.current_pos:
                            self.utility[i.current_pos[0]][i.current_pos[1]] = float("inf")

        for neighbor in neighbors:
            col, row = neighbor
            distance = self.utility[col][row]
            if distance < current_min_distance:
                current_min_distance = distance
                current_selected_neighbor = neighbor

        self.utility = []

        return current_min_distance, current_selected_neighbor
