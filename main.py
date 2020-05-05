from tkinter import *
from classes.cms import CMS
import math
import sys

# Create the root window
root = Tk()
root.title("TUM-MLCMS-1 Group C")
root.maxsize(1500, 1500)
root.resizable(True, True)

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

top_frame = Frame(root)

simulation_control_button_text = StringVar()
simulation_control_button = Button(top_frame, textvariable=simulation_control_button_text,
                                      command=on_click_simulation_control_button)
simulation_control_button_text.set("Run")
simulation_control_button.pack(side=LEFT)

# Create a label for showing the current step
current_step_text = StringVar()
current_step_label = Label(top_frame, textvariable=current_step_text)
current_step_text.set("Current Step: 0")
current_step_label.pack(side=RIGHT)

top_frame.pack(side=TOP, padx=10, pady=10)

read_file_name = "helper/data/rimea_test_7.in"
if len(sys.argv) > 1:
    read_file_name = sys.argv[1]

# Create the canvas
board = CMS(read_file_name)
board.pack()
board.set_step_text(current_step_text)

root.mainloop()
