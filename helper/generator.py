import math
from random import randint


def generate_circular_pedestrians():
    output_file = open("circular_test.in", 'w+')

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


def generate_test_1():
    output_file = open("rimea_test_1.in", 'w+')

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


def generate_test_4():

    width = 500
    height = 13

    output_file = open("rimea_test_4.in", 'w+')

    output_file.write(f"GRID({width+2},{height+2})\n")

    coordinates = set()

    coordinates.add((width, int(height/2)))

    while len(coordinates) <= 1000:
        x, y = randint(1, width), randint(1, height)
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

    output_file.write(f"T({width},{int(height/2)})\n")


def generate_test_6():
    output_file = open("rimea_test_6.in", 'w+')

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


def generate_test_7():
    output_file = open("rimea_test_7.in", 'w+')

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

generate_circular_pedestrians()
generate_test_1()
generate_test_4()
generate_test_6()