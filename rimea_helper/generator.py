import math

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
    output_file = open("rimea_test_4.in", 'w+')

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
generate_test_6()