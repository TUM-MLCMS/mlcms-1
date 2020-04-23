import tkinter as tk
from classes.cms import CMS

root = tk.Tk()
root.title("CMS")
root.resizable(False, False)

board = CMS()
board.pack()

root.mainloop()
