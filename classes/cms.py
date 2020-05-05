from tkinter import *
from classes.pedestrian import Pedestrian
from classes.obstacle import Obstacle
from classes.target import Target
from classes.grid import Grid
import math


# Main class of the CMS
class CMS(Frame):
    # Resets the initial simulation values
    def setup_initial_state(self):
        self.is_running = False
        self.is_finished = False
        self.step = 0
        self.success = False
        self.utility = []  # Utility matrix that takes into account also the positions of the pedestrians.

        self.debug_step = False # This enables debugging in which only one pedestrian moves per step
        self.current_pedestrian_index = 0

        self.simulation_grid = Grid(0, 0)
        self.simulation_grid.read_from_file(self.file_to_read)
        self.simulation_grid.create_euclidean_distance_field()
        self.simulation_grid.create_dijkstra_distance_field()

    def __init__(self, filename, master=None):

        Frame.__init__(self, master)
        Pack.config(self)

        self.offset = {'V': 20, 'H': 20, 'D': 2}  # Vertical & Horizontal gap of the canvas, offset for drawing objects.
        self.current_step_text = None
        self.control_button = None
        self.show_coordinates = False
        self.show_ids = False

        self.width = 3000
        self.height = 400
        self.file_to_read = filename

        self.canvas = Canvas(self,
                           width=self.width,
                           height=self.height,
                           background="black",
                           highlightthickness=0,
                           scrollregion=(0, 0, self.width, self.height))

        # Scrollbar.
        self.canvas.scrollX = Scrollbar(self, orient=HORIZONTAL)
        self.canvas['xscrollcommand'] = self.canvas.scrollX.set
        self.canvas.scrollX['command'] = self.canvas.xview
        self.canvas.scrollX.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT)

        self.setup_initial_state()

        self.cell_size = min((self.width - self.offset['H']) / self.simulation_grid.cols, (self.height - self.offset['V']) / self.simulation_grid.rows)

        # New offset values set to center the simulation.
        self.offset['V'] = (self.height - self.simulation_grid.rows * self.cell_size) / 2
        self.offset['H'] = (self.width - self.simulation_grid.cols * self.cell_size) / 2

        self.rect_start_x = self.offset['H']
        self.rect_start_y = self.offset['V']
        self.rect_end_x = self.width - self.offset['H']
        self.rect_end_y = self.height - self.offset['V']
        self.draw()

    # Start or stop the simulation
    def start_or_stop(self, button):
        self.is_running = not self.is_running
        self.control_button = button
        self.loop()

    # Start or stop the simulation
    def reset(self, text, button):
        self.setup_initial_state()
        self.control_button = button

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
        self.canvas.delete("all")

        # Draw the borders.
        self.canvas.create_rectangle(
            self.rect_start_x - self.offset['D'] * 2,
            self.rect_start_y - self.offset['D'] * 2,
            self.rect_end_x + self.offset['D'] * 2,
            self.rect_end_y + self.offset['D'] * 2,
            outline="#FFFFFF"
        )

        # Call the evaluation, which moves and renders the current state.
        if not self.is_finished and self.is_running:
            self.evaluate()

        # Rendering Obstacles.
        for obstacle in self.simulation_grid.elements['O']:
            coord_x, coord_y = self.coordinate(*obstacle.current_pos)
            self.fill(coord_x, coord_y, obstacle.color, "O")

        # Rendering Target.
        coord_x, coord_y = self.coordinate(*self.simulation_grid.elements['T'].current_pos)
        self.fill(coord_x, coord_y, self.simulation_grid.elements['T'].color, "T")

        # Rendering Pedestrians.
        for i, pedestrian in enumerate(self.simulation_grid.elements['P']):
            coord_x, coord_y = self.coordinate(*pedestrian.current_pos)
            self.fill(coord_x, coord_y, pedestrian.color, str(i + 1))

        # Print coordinates of cells. Very useful for development.
        if self.show_coordinates:
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
        self.canvas.create_rectangle(x + self.offset['D'],
                              y + self.offset['D'],
                              x + self.cell_size - self.offset['D'],
                              y + self.cell_size - self.offset['D'],
                              fill=color)

        if self.show_ids:
            self.create_text(x + self.offset['D'] + self.cell_size / 2,
                             y + self.offset['D'] + self.cell_size / 2,
                             fill="#FFFFFF",
                             text=i)

    # Evaluates the next state of the system.
    def evaluate(self):
        # Simulate Pedestrian movement
        if self.debug_step:
            pedestrians = [self.simulation_grid.elements['P'][self.current_pedestrian_index]]
        else:
            pedestrians = self.simulation_grid.elements['P']

        for pedestrian in pedestrians:
            if not pedestrian.has_arrived:
                distance, move_target = self.get_move_coordinate(pedestrian)
                pedestrian.move(move_target)
                if distance == 0:
                    pedestrian.has_arrived = True

        average_speed = 0
        for pedestrian in pedestrians:
            average_speed = average_speed + pedestrian.get_speed()
        average_speed = average_speed / len(pedestrians)
        print(f"Average Speed: {average_speed}")

        # Render the current pedestrians next move with red. For tracking.
        if self.debug_step:
            coord_x, coord_y = self.coordinate(*pedestrians[0].current_pos)
            self.fill(coord_x, coord_y, "#CC0000", str(self.current_pedestrian_index + 1))

        # Check success condition
        self.success = True
        for pedestrian in self.simulation_grid.elements['P']:
            if not pedestrian.has_arrived:
                self.success = False
                break

        # Assign the next pedestrian
        if not self.success:
            self.current_pedestrian_index = (self.current_pedestrian_index + 1) % len(self.simulation_grid.elements['P'])
            while self.simulation_grid.elements['P'][self.current_pedestrian_index].has_arrived:
                self.current_pedestrian_index = (self.current_pedestrian_index + 1) % len(self.simulation_grid.elements['P'])

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

        for d in self.simulation_grid.dijkstra_field:
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