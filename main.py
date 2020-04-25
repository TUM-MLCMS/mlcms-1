import tkinter as tk
from classes.cms import CMS
import math
import sys

# Create the root window
root = tk.Tk()
root.title("CMS")
root.resizable(False, False)


# Create a simulation controlling button
def on_click_simulation_control_button():
    if board.is_running:
        stop()

    elif board.is_finished:
        reset()

    else:
        start()


def start():
    simulation_control_button_text.set("Stop")
    board.start_or_stop(simulation_control_button_text)


def stop():
    simulation_control_button_text.set("Start")
    board.start_or_stop(simulation_control_button_text)


def reset():
    current_step_text.set("Current Step: 0")
    simulation_control_button_text.set("Stop")
    board.reset(current_step_text, simulation_control_button_text)


def circular_pedestrians():
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


#circular_pedestrians()

simulation_control_button_text = tk.StringVar()
simulation_control_button = tk.Button(root, textvariable=simulation_control_button_text,
                                      command=on_click_simulation_control_button)
simulation_control_button_text.set("Run")
simulation_control_button.grid(row=0, column=0, sticky=tk.W)

# Create a label for showing the current step
current_step_text = tk.StringVar()
current_step_label = tk.Label(root, textvariable=current_step_text)
current_step_text.set("Current Step: 0")
current_step_label.grid(row=0, column=1, sticky=tk.W)

read_file_name = "default.in"
if len(sys.argv) > 1:
    read_file_name = sys.argv[1]

# Create the canvas
board = CMS(read_file_name)
board.grid(row=1, column=0, columnspan=2)
board.set_step_text(current_step_text)

root.mainloop()
