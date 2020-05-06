from tkinter import *
from classes.cms import CMS
import sys

# Create the root window
root = Tk()
root.title("TUM-MLCMS-1 Group C")
root.maxsize(1500, 1500)
root.resizable(True, True)

# Create a simulation controlling button
def on_click_control_button():
    if board.is_running:
        stop()
    elif board.is_finished:
        reset()
    else:
        start()

# Starts the simulation.
def start():
    control_button_text.set("Stop")
    board.start_or_stop(control_button_text)

#Stops the simulation.
def stop():
    control_button_text.set("Start")
    board.start_or_stop(control_button_text)

# Resets the simulation.
def reset():
    current_step_text.set("Current Step: 0")
    control_button_text.set("Stop")
    board.reset(current_step_text, control_button_text)

# Top and bottom frames.
top_frame = Frame(root)
bottom_frame = Frame(root)

# Button for controlling simulation.
control_button_text = StringVar()
control_button = Button(top_frame, textvariable=control_button_text,command=on_click_control_button)
control_button_text.set("Run")
control_button.pack(side=LEFT)

# Create a label for showing the current step.
current_step_text = StringVar()
current_step_label = Label(top_frame, textvariable=current_step_text)
current_step_text.set("Current Step: 0")
current_step_label.pack(side=RIGHT)

# Packing frames.
top_frame.pack(side=TOP, padx=10, pady=10)
bottom_frame.pack(side=BOTTOM, padx=10, pady=10)

# Check if any choice made, else; just show a welcome screen.
if len(sys.argv) > 1:
    id = sys.argv[1]

# Read files for test selection.
if id == '1':
    read_file_name = "helpers/data/rimea_test_1.in"
elif id == '4':
    read_file_name = "helpers/data/rimea_test_4.in"
elif id == '6':
    read_file_name = "helpers/data/rimea_test_6.in"
elif id == '7':
    read_file_name = "helpers/data/rimea_test_7.in"
elif id == 'circular':
    read_file_name = "helpers/data/circular_test.in"
elif id == 'chicken':
    read_file_name = "helpers/data/chicken_test.in"
else:
    read_file_name = "helpers/data/welcome.in"

# Create the canvas.
board = CMS(read_file_name, id)
board.pack()
board.set_step_text(current_step_text)

# Sending the text objects.
if id in ['1', '7']:
    speed_text = StringVar()
    speed_label = Label(bottom_frame, textvariable=speed_text)
    speed_text.set("Average Speed: 0")
    speed_label.pack(side=RIGHT)
    board.set_average_speed_text(speed_text)
elif id == '4':
    read_file_name = "helpers/data/rimea_test_4.in"
    cp1_text = StringVar()
    cp1_label = Label(bottom_frame, textvariable=cp1_text)
    cp1_text.set("Average Speed at Control Point #1: 0")
    cp1_label.pack(side=TOP)
    cp2_text = StringVar()
    cp2_label = Label(bottom_frame, textvariable=cp2_text)
    cp2_text.set("Average Speed at Control Point #2: 0")
    cp2_label.pack(side=TOP)
    mcp_text = StringVar()
    mcp_label = Label(bottom_frame, textvariable=mcp_text)
    mcp_text.set("Average Speed at Main Measuring Point: 0")
    mcp_label.pack(side=TOP)
    board.set_cp1_text(cp1_text)
    board.set_cp2_text(cp2_text)
    board.set_mcp_text(mcp_text)

# Main loop.
root.mainloop()
