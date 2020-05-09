class Measure:
    def __init__(self, position, tag, id, height):
        self.tag = tag
        self.id = id
        self.color = ""
        self.pos = position
        self.cells = []

        if self.tag == 'MM':
            self.color = "#404040"
        elif self.tag == 'CM':
            self.color = "#2E2E2E"

        # If height is greater than or equal to 6 meters. Adds the offset for borders as well.
        if height >= 17:
            # Defines a 2x2 meters area for control points.
            for i in range(-2, 3):
                for j in range(-2, 3):
                    self.cells.append((position[0] + i, position[1] + j))

        # If height is greater than or equal to 4 meters.
        elif height >= 11:
            # Defines a 1.2x1.2 meters area for control points.
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.cells.append((position[0] + i, position[1] + j))

        # If height is less than 4 meters.
        else:
            # Defines a 0.4x0.4 meters area for control points.
            self.cells.append((position[0], position[1]))

