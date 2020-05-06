class Measure:
    def __init__(self, position, tag, id):
        self.tag = tag
        self.id = id
        self.color = ""
        self.pos = position
        self.cells = []

        if self.tag == 'MM':
            self.color = "#404040"
        elif self.tag == 'CM':
            self.color = "#2E2E2E"

        # Defines a 2x2 meters area for control points.
        for i in range(-2,3):
            for j in range(-2,3):
                self.cells.append((position[0] + i, position[1] + j))
