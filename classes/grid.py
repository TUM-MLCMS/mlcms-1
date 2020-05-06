from classes.measure import Measure
from classes.pedestrian import Pedestrian
from classes.obstacle import Obstacle
from classes.target import Target
import math

class Grid:
    rows = 0
    cols = 0
    tiles = []
    elements = {}

    def __init__(self, rows, cols):
        self.elements = elements = {
            'P': [],
            'T': {},
            'O': [],
            'M': []
        }
        self.rows = rows
        self.cols = cols
        self.tiles = [[0 for x in range(rows)] for y in range(rows)]
        self.distance_field = []

    # Reads and processes the input file.
    def read_from_file(self, filename):
        input_file = open(filename, 'r')
        lines = input_file.readlines()
        for line in lines:
            cell_type = line.split("(")[0]
            parenthesis = line.split('(', 1)[1].split(')')[0]
            values = list(map(int, parenthesis.split(",")))

            if cell_type == "GRID":
                self.cols = values[0]
                self.rows = values[1]
            elif cell_type == "P":
                self.elements['P'].append(Pedestrian((values[0], values[1])))
            elif cell_type == "T":
                self.elements['T'] = Target((values[0], values[1]))
            elif cell_type == "O":
                self.elements['O'].append(Obstacle((values[0], values[1])))
            elif cell_type == "CM1":
                self.elements['M'].append(Measure((values[0], values[1]), 'CM', 1))
            elif cell_type == "CM2":
                self.elements['M'].append(Measure((values[0], values[1]), 'CM', 2))
            elif cell_type == "MM":
                self.elements['M'].append(Measure((values[0], values[1]), 'MM', 0))

    # Create a distance field with euclidean distance.
    def create_euclidean_distance_field(self):
        self.distance_field = [[0] * self.rows for col in range(self.cols)]
        target_col, target_row = self.elements['T'].current_pos

        for row in range(self.rows):
            for col in range(self.cols):
                self.distance_field[col][row] = math.sqrt(pow(target_col - col, 2) + pow(target_row - row, 2))

        for o in self.elements['O']:
            col, row = o.current_pos
            self.distance_field[col][row] = float("inf")

    # Gets all valid neighbors of a cell.
    def get_all_neighbors(self, pos):
        neighbors = []

        self_col, self_row = pos
        start_col = max(0, self_col - 1)
        start_row = max(0, self_row - 1)

        end_col = min(self_col + 1, self.cols - 1)
        end_row = min(self_row + 1, self.rows - 1)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                is_obstacle = False
                for o in self.elements['O']:
                    obstacle_col, obstacle_row = o.current_pos
                    if obstacle_col == col and obstacle_row == row:
                        is_obstacle = True
                        break
                if not is_obstacle:
                    neighbors.append((col, row))

        return neighbors

    # Gets the cell with smallest distance value.
    def get_smallest_distance_cell(self, visited_set):
        current_selected_cell = None
        current_min_distance = float("inf")

        for row in range(self.rows):
            for col in range(self.cols):
                if self.dijkstra_field[col][row] < current_min_distance and (col, row) not in visited_set:
                    current_selected_cell = (col, row)
                    current_min_distance = self.dijkstra_field[col][row]

        return current_selected_cell

    # Create a dijkstra distance field for avoiding obstacles.
    def create_dijkstra_distance_field(self):
        self.dijkstra_field = [[float("inf")] * self.rows for col in range(self.cols)]

        target_col, target_row = self.elements['T'].current_pos
        self.dijkstra_field[target_col][target_row] = 0
        
        visited_set = set()
        
        while True:
            node = self.get_smallest_distance_cell(visited_set)
            if node == None:
                break
            visited_set.add(node)
            node_col, node_row = node
            node_neighbors = self.get_all_neighbors(node)
            for neighbor in node_neighbors:
                neighbor_col, neighbor_row = neighbor
                new_distance = self.dijkstra_field[node_col][node_row] + math.sqrt(pow(node_col - neighbor_col, 2) + pow(node_row - neighbor_row, 2))
                if new_distance < self.dijkstra_field[neighbor_col][neighbor_row]:
                    self.dijkstra_field[neighbor_col][neighbor_row] = new_distance