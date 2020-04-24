import tkinter as tk
from classes.cms import CMS

#Create the root window
root = tk.Tk()
root.title("CMS")
root.resizable(False, False)

#Create a simulation controlling button
def on_click_simulation_control_button():
    board.start_or_stop()
    if board.is_running:
        simulation_control_button_text.set("Stop")
    else:
        simulation_control_button_text.set("Run")

simulation_control_button_text = tk.StringVar()
simulation_control_button = tk.Button(root, textvariable=simulation_control_button_text, command = on_click_simulation_control_button)
simulation_control_button_text.set("Run")
simulation_control_button.grid(row=0,column=0, sticky=tk.W)

#Create a label for showing the current step
current_step_text = tk.StringVar()
current_step_label = tk.Label(root, textvariable=current_step_text)
current_step_text.set("Current Step: 0")
current_step_label.grid(row=0, column=1, sticky=tk.W)

#Create the canvas
board = CMS()
board.grid(row=1, column=0, columnspan=2)
board.set_step_text(current_step_text)

root.mainloop()
