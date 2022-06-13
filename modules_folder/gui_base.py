# External Imports
from tkinter import *
from tkinter import ttk
from sys import platform

# Internal Imports
from modules_folder.global_vars import *
from modules_folder.config_vars import *

root = Tk()
root.title("VirtuVirus")
root.iconname("VirtuVirus")
root.resizable(False, False)

# Set icon
if "win" in platform:
	root.wm_iconbitmap(default="assets/icon.ico")
else:
	img = PhotoImage(file='assets/icon.png')
	root.tk.call('wm', 'iconphoto', root._w, img)

# and theme
style = ttk.Style(root)
if "win" in platform:
	style.theme_use('vista')
else:
	style.theme_use('clam')

# Create frame at the top
frame = ttk.Frame(root)
frame.pack(side=TOP)

# Create canvas
canvas = Canvas(frame, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack(side=RIGHT)

# Add controls to the left of the frame
controls = ttk.Frame(frame)
controls.pack(side=LEFT, padx=10)

# Add controls label
controls_label = ttk.Label(controls, text="Controls")
controls_label.pack(pady=10)