class Pedestrian:
    def __init__(self, start_pos):
        self.tag = 'P'
        self.color = "#009900"
        self.start_pos = start_pos
        self.current_pos = start_pos

    # Moves the pedestrian to the desired direction.
    def move(self, direction):
        if direction == 'R':
            self.current_pos = (self.current_pos[0] + 1, self.current_pos[1])

        elif direction == 'L':
            self.current_pos = (self.current_pos[0] - 1, self.current_pos[1])

        elif direction == 'U':
            self.current_pos = (self.current_pos[0], self.current_pos[1] + 1)

        elif direction == 'D':
            self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)

        elif direction == 'SUCCESS':
            return

        else:
            print("WRONG DIRECTION INPUT GIVEN.")
