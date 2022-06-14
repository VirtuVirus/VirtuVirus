# External Imports
import tkinter as tk
import tkinter.ttk as ttk

def createButton(root, location, text, command = None, arguments = None, padding = (4, 4, 4, 4)):
	if command == "pass" or command == None:
		button = ttk.Button(root, text=text, padding=padding)
	else:
		button = ttk.Button(root, text=text, padding=padding, command=lambda: command(arguments))
	button.pack(side=location)
	return button

def createFrame(root, location, padding = (0, 0, 0, 0), fill = None, expand = None, anchor = None, ipadx = None, ipady = None):
	frame = ttk.Frame(root, padding=padding)
	frame.pack(side=location, fill = fill, expand = expand, anchor = anchor, ipadx = ipadx, ipady = ipady)
	return frame