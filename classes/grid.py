from classes.pedestrian import Pedestrian
from classes.obstacle import Obstacle
from classes.target import Target
import math

class Grid:
    rows = 0
    cols = 0
    tiles = []
    elements = {
        'P': [],
        'T': {},
        'O': []
    }

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tiles = [[0 for x in range(rows)] for y in range(rows)]

    def read_from_file(self, filename):
        input_file = open(filename, 'r') 
        lines = input_file.readlines()
        for line in lines:
            cell_type = line.split("(")[0]
            paranthesis = line.split('(', 1)[1].split(')')[0]
            values = list(map(int, paranthesis.split(",")))

            if cell_type == "GRID":    
                self.cols = values[0]
                self.rows = values[1]
            elif cell_type == "P":
                self.elements['P'].append(Pedestrian((values[0], values[1])))
            elif cell_type == "T":
                self.elements['T'] = Target((values[0], values[1]))
            elif cell_type == "O":
                self.elements['O'].append(Obstacle((values[0], values[1])))

    def create_distance_field(self):
        self.distance_field = [[0] * self.cols for row in range(self.rows)]
        target_col, target_row = self.elements['T'].current_pos
        
        for row in range(self.rows):
            for col in range(self.cols):
                self.distance_field[row][col] = math.sqrt(pow(target_col - col, 2) + pow(target_row - row, 2))