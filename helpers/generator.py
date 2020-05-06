import math
from random import randint

class Generator():

    def __init__(self, width=200, height=10, density=1, id=None):

        self.width = width
        self.height = height
        self.density = density
        self.id = id

        print(type(self.width))

        if self.id == '1':
            self.generate_test_1()
        elif self.id == '4':
            self.generate_test_4(w=self.width, h=self.height, density=self.density, default=False)
        elif self.id == '6':
            self.generate_test_6()
        elif self.id == '7':
            self.generate_test_7()
        elif self.id == 'circular':
            self.generate_circular_pedestrians()
        elif self.id == 'chicken':
            pass
        elif self.id == 'bottleneck':
            pass
        else:
            self.generate_welcome_page()


    def generate_welcome_page(self):
        output_file = open("data/welcome.in", 'w+')

        # Letter C
        for i in range(3, 7):
            output_file.write(f"P({i},3)\n")
            output_file.write(f"P({i},9)\n")
        for i in range(4, 9):
            output_file.write(f"P(3,{i})\n")

        # Letter M
        for i in range(8, 13):
            output_file.write(f"P({i},3)\n")
        for i in range(4, 10):
            output_file.write(f"P(8,{i})\n")
            output_file.write(f"P(12,{i})\n")
        for i in range(4, 9):
            output_file.write(f"P(10,{i})\n")

        # Letter S
        for i in range(14, 18):
            output_file.write(f"P({i},3)\n")
            output_file.write(f"P({i},6)\n")
            output_file.write(f"P({i},9)\n")
        for i in range(4, 6):
            output_file.write(f"P(14,{i})\n")
        for i in range(7, 9):
            output_file.write(f"P(17,{i})\n")

        # Line
        for i in range(3,18):
            output_file.write(f"O({i},11)\n")

        output_file.write("GRID(21,15)\n")
        output_file.write("T(10,13)\n")


    def generate_circular_pedestrians(self):
        output_file = open("data/circular_test.in", 'w+')

        coordinates = []
        R = 24
        X = int(R)
        for x in range(-X, X + 1):
            Y = int((R * R - x * x) ** 0.5)
            for y in range(-Y, Y + 1):
                if math.sqrt(pow(x, 2) + pow(y, 2)) > 23:
                    coordinates.append("P(" + str(x + 24) + "," + str(y + 24) + ")\n")

        output_file.write("GRID(50,50)\n")
        output_file.write("T(25,25)\n")
        output_file.writelines(coordinates)


    def generate_test_1(self):
        output_file = open("data/rimea_test_1.in", 'w+')

        output_file.write("GRID(102,7)\n")

        for i in range(102):
            output_file.write(f"O({i},0)\n")

        for i in range(5):
            output_file.write(f"O(0,{i + 1})\n")

        for i in range(102):
            output_file.write(f"O({i},6)\n")

        for i in range(5):
            output_file.write(f"O(101,{i + 1})\n")

        output_file.write(f"P(1,3)\n")

        output_file.write(f"T(100,3)\n")


    def generate_test_4(self, w=200, h=10, density = 0.2, default=True):

        width = int(w*2.5)
        height = int(h*2.5)

        if  default:
            output_file = open("data/rimea_test_4.in", 'w+')
        else:
            output_file = open("data/rimea_test_4_d_" + str(density) + "_w_" + str(w) + "_h_" + str(h) + ".in", 'w+')


        output_file.write(f"GRID({width+2},{height+2})\n")

        coordinates = set()

        while len(coordinates) <= w*h*density:
            x, y = randint(1, width), randint(1, height)
            if (x != 50) and (y != 25):
                coordinates.add((x, y))

        for i in range(width+2):
            output_file.write(f"O({i},0)\n")

        for i in range(height):
            output_file.write(f"O(0,{i + 1})\n")

        for i in range(width+2):
            output_file.write(f"O({i},{height+1})\n")

        for i in range(height):
            output_file.write(f"O({width+1},{i + 1})\n")

        for c in coordinates:
            output_file.write(f"P({c[0]},{c[1]})\n")

        output_file.write(f"MM({int(width / 2)},{int(height / 2)})\n")

        output_file.write(f"CM1({int(0.45*width)},{int(height / 2)})\n")

        output_file.write(f"CM2({int(width / 2)},{int((height / 2) + 5)})\n")

        output_file.write(f"T({width},{int(height/2)})\n")


    def generate_test_6(self):
        output_file = open("data/rimea_test_6.in", 'w+')

        output_file.write("GRID(30,30)\n")

        for i in range(30):
            output_file.write(f"O({i},29)\n")
            output_file.write(f"O(29,{i})\n")

        for i in range(24):
            output_file.write(f"O({i},23)\n")

        for i in range(24):
            output_file.write(f"O(23,{23-i})\n")

        skip = 75 // 20
        offset = 0
        for ped in range(20):
            output_file.write(f"P({offset//5},{28 - offset % 5})\n")
            offset = offset + skip
        output_file.write(f"T(25,0)\n")


    def generate_test_7(self):
        width = 50
        height = 50

        output_file = open("data/rimea_test_7.in", 'w+')

        output_file.write(f"GRID({width + 2},{height + 2})\n")

        coordinates = set()

        while len(coordinates) <= 50:
            x, y = randint(1, width), randint(1, height)
            if (x != 50) and (y != 25):
                coordinates.add((x, y))

        for i in range(width + 2):
            output_file.write(f"O({i},0)\n")

        for i in range(height):
            output_file.write(f"O(0,{i + 1})\n")

        for i in range(width + 2):
            output_file.write(f"O({i},{height + 1})\n")

        for i in range(height):
            output_file.write(f"O({width + 1},{i + 1})\n")

        for c in coordinates:
            output_file.write(f"P({c[0]},{c[1]})\n")

        output_file.write(f"T({width},{int(height / 2)})\n")

    # generate_welcome_page()
    # generate_circular_pedestrians()
    # generate_test_1()
    # generate_test_4()
    # generate_test_4(w=1000, h=10, density=1, default=False)
    # generate_test_4(w=200, h=10, density=1, default=False)
    # generate_test_4(w=200, h=10, density=2, default=False)
    # generate_test_4(w=200, h=10, density=3, default=False)
    # generate_test_4(w=200, h=10, density=4, default=False)
    # generate_test_4(w=200, h=10, density=5, default=False)
    # generate_test_4(w=200, h=10, density=0.1, default=False)
    # generate_test_4(w=200, h=10, density=0.2, default=False)
    # generate_test_4(w=200, h=10, density=0.3, default=False)
    # generate_test_4(w=200, h=10, density=0.4, default=False)
    # generate_test_4(w=200, h=10, density=0.5, default=False)
    # generate_test_6()
    # generate_test_7()