
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

generate_test_1()
generate_test_6()