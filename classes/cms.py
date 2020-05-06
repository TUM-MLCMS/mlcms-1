from random import randint
from tkinter import *
import numpy
import csv
from classes.grid import Grid

# Main class of the CMS
class CMS(Frame):

    # Resets the initial simulation values
    def setup_initial_state(self):
        self.is_running = False # True if simulation is running.
        self.is_finished = False # True if simulation is finished.
        self.step = 0 # Current step.
        self.success = False # True if all pedestrians has reached the target.
        self.utility = []  # Utility matrix that takes into account also the positions of the pedestrians.
        self.average_speed = {} # Average speeds of pedestrians at measuring areas.

        self.debug_step = False # This enables debugging in which only one pedestrian moves per step
        self.current_pedestrian_index = 0 # Index of the current pedestrian.

        self.simulation_grid = Grid(0, 0) # Simulation grid, information will be fetched from input file.
        self.simulation_grid.read_from_file(self.file_to_read) # Reads the input.
        self.simulation_grid.create_euclidean_distance_field() # Creates euclidean distance field.
        self.simulation_grid.create_dijkstra_distance_field() # Creates dijkstra distance field.

        # Assigning ages and setting speeds are done for only test #7, this can easily be changed for others here.
        if self.test_id == '7':
            self.set_ages()
            self.set_speeds()

        # Populates the average speed dictionary for control points with zeros.
        for i in range(len(self.simulation_grid.elements['M'])):
            self.average_speed[i] = 0

    def __init__(self, filename, id=None, master=None):

        Frame.__init__(self, master)
        Pack.config(self)

        self.offset = {'V': 20, 'H': 20, 'D': 2}  # Vertical & Horizontal gap of the canvas, offset for drawing objects.
        self.current_step_text = None # Shows the current step.
        self.average_speed_text = None  # Average speed of all pedestrians, for test #1.
        self.cp1_text = None  # Shows the average speed at CP #1.
        self.cp2_text = None  # Shows the average speed at CP #2.
        self.mcp_text = None  # Shows the average speed at Main Control Point.
        self.control_button = None # Control button object to be fetched from GUI.
        self.show_coordinates = False # For debugging.
        self.show_ids = False # For debugging.
        self.test_id = None # ID of the current test.
        self.loop_interval = 100 #Interval between steps.

        if id == '1':
            self.test_id = id
            self.width = 1200
            self.height = 200
        elif id == '4':
            self.test_id = id
            self.width = 5000
            self.height = 400
            self.offset['D'] = 0
            self.loop_interval = 1
        elif id == '6':
            self.test_id = id
            self.width = 600
            self.height = 600
        elif id == '7':
            self.test_id = id
            self.width = 600
            self.height = 600
        elif id == 'circular':
            self.test_id = id
            self.width = 600
            self.height = 600
        elif id == 'chicken':
            self.test_id = id
            self.width = 600
            self.height = 600
        else:
            self.test_id = id
            self.width = 800
            self.height = 600

        # Readfile.
        self.file_to_read = filename

        # Canvas.
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
        self.canvas.pack(side=BOTTOM)

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

    # Get simulation step text object from the GUI.
    def set_step_text(self, current_step_text):
        self.current_step_text = current_step_text

    # Get the average speed text object from the GUI, for test #1.
    def set_average_speed_text(self, average_speed_text):
        self.average_speed_text = average_speed_text

    # Get the Control Point #1 text object from the GUI, for test #4.
    def set_cp1_text(self, control_point_text):
        self.cp1_text = control_point_text

    # Get the Control Point #2 text object from the GUI, for test #4.
    def set_cp2_text(self, control_point_text):
        self.cp2_text = control_point_text

    # Get the Main Control Point text object from the GUI, for test #4.
    def set_mcp_text(self, control_point_text):
        self.mcp_text = control_point_text

    # Loop.
    def loop(self):
        if self.is_running:
            self.step = self.step + 1
            self.current_step_text.set(f"Current Step: {self.step}")
            self.draw()
            self.after(self.loop_interval, self.loop)

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

        # Rendering Measure Areas.
        for measure in self.simulation_grid.elements['M']:
            for cell in measure.cells:
                coord_x, coord_y = self.coordinate(*cell)
                self.fill(coord_x, coord_y, measure.color, "M")

        # Rendering Pedestrians.
        for i, pedestrian in enumerate(self.simulation_grid.elements['P']):
            coord_x, coord_y = self.coordinate(*pedestrian.current_pos)
            self.fill(coord_x, coord_y, pedestrian.color, str(i + 1))

        # Print coordinates of cells. Very useful for development.
        if self.show_coordinates:
            for i in range(0, self.simulation_grid.rows):
                for j in range(0, self.simulation_grid.cols):
                    x, y = self.coordinate(i, j)

                    self.canvas.create_text(x + self.offset['D'] + self.cell_size / 2,
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
            self.canvas.create_text(x + self.offset['D'] + self.cell_size / 2,
                             y + self.offset['D'] + self.cell_size / 2,
                             fill="#FFFFFF",
                             text=i)

    # Evaluates the next state of the system.
    def evaluate(self):
        # Simulate Pedestrian movement.
        if self.debug_step:
            pedestrians = [self.simulation_grid.elements['P'][self.current_pedestrian_index]]
        else:
            pedestrians = self.simulation_grid.elements['P']

        # Move the pedestrian.
        for pedestrian in pedestrians:
            if not pedestrian.has_arrived:
                distance, move_target = self.get_move_coordinate(pedestrian)
                is_moved = pedestrian.move(move_target)
                if distance == 0 and is_moved:
                    pedestrian.has_arrived = True

        # Print average speed for tests #1 and #7.
        if self.test_id in ['1', '7']:
            average_speed = 0
            for pedestrian in pedestrians:
                average_speed = average_speed + pedestrian.get_speed()
            average_speed = average_speed / len(pedestrians)
            self.average_speed_text.set(f"Average Speed: {round(average_speed, 3)} m/s")

        # Print average speeds at control points for test #4.
        if self.test_id == '4':
            count = {}
            for i in range(len(self.simulation_grid.elements['M'])):
                count[i] = 0
            for i, pedestrian in enumerate(pedestrians):
                for j, measure in enumerate(self.simulation_grid.elements['M']):
                    if pedestrian.current_pos in measure.cells:
                        self.average_speed[j] = self.average_speed[j] + pedestrian.get_speed()
                        count[j] += 1
            # For the flow calculation, since control points are 1x1 meters, densitiy is 'count[i]' and Flow = Speed * Density
            for i, cp in enumerate(self.simulation_grid.elements['M']):
                if cp.id == 1:
                    if count[i] == 0:
                        self.cp1_text.set(
                            f"Control Point #1: 0 m/s | 0 P/m.s")
                    else:
                        self.cp1_text.set(
                            f"Control Point #1: {round(self.average_speed[i] / count[i], 3)} m/s | {round(self.average_speed[i], 3)} P/m.s")
                elif cp.id == 2:
                    if count[i] == 0:
                        self.cp2_text.set(
                            f"Control Point #2: 0 m/s | 0 P/m.s")
                    else:
                        self.cp2_text.set(
                            f"Control Point #2: {round(self.average_speed[i] / count[i], 3)} m/s | {round(self.average_speed[i], 3)} P/m.s")
                else:
                    if count[i] == 0:
                        self.mcp_text.set(
                            f"Main Measuring Point: 0 m/s | 0 P/m.s")
                    else:
                        self.mcp_text.set(
                            f"Main Measuring Point: {round(self.average_speed[i] / count[i], 3)} m/s | {round(self.average_speed[i], 3)} P/m.s")

            for i in range(len(self.simulation_grid.elements['M'])):
                self.average_speed[i] = 0

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

            # Output the ages and average speeds for test #7.
            if self.test_id == '7':
                output = open('outputs/test_7.csv', 'w', newline='')
                writer = csv.writer(output, delimiter='\t')
                for i, pedestrian in enumerate(self.simulation_grid.elements['P']):
                    writer.writerow([pedestrian.age, round(pedestrian.get_speed(),3)])

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

    # Approximate distribution of maximum speeds according to experimental data.
    def set_speeds(self):
        pedestrians = self.simulation_grid.elements['P']

        for pedestrian in pedestrians:

            if pedestrian.age<=20:
                mean = 1.5 + (pedestrian.age-18)/20
                std = 0.3
            elif pedestrian.age>20 and pedestrian.age<=40:
                mean = 1.6 - (pedestrian.age - 20)/200
                std = 0.25
            elif pedestrian.age>40 and pedestrian.age<=60:
                mean = 1.5 - (pedestrian.age-40)/100
                std = 0.25
            else:
                mean = 1.3 - (pedestrian.age-60)/35
                std = 0.1

            pedestrian.max_speed = numpy.random.normal(mean, std)

    # Assign age values to pedestrians.
    def set_ages(self):
        pedestrians = self.simulation_grid.elements['P']

        for pedestrian in pedestrians:
            pedestrian.age = randint(18, 80)