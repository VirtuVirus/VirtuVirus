# External Imports
import tkinter as tk
import tkinter.ttk as ttk

# Internal Imports
from modules import configVars

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

def generateCanvass(CanvasRoot, number, width, height, windowRoot, hasInfectiveContainer = False):
	canvasses = []
	i = 0
	j = 0

	temp=number

	while temp > 0:
		canvas = tk.Canvas(CanvasRoot, width=width, height=height, bg="white")
		canvas.grid(row=j, column=i, sticky="NSEW", padx=2, pady=2)
		canvas.grid_propagate(False)
		temp -= 1
		i+=1

		if i >= 5:
			i = 0
			j += 1
		
		canvasses.append({"simulationZone": canvas, "agents": [], "saneAgents": [], "infectedAgents": [], "immuneAgents": [], "deadAgents": [], "connectedThreads": [], "isInfectiveContainer": False})
	
	if hasInfectiveContainer:
		canvas.config(highlightthickness=2, highlightbackground="red")
		canvasses[-1]["isInfectiveContainer"] = True
		
	# Adapt minimal resolution of windowRoot
	windowRoot.minsize(int(width*5+200), max(int(height*j+55), configVars.HEIGHT))


	print("Generated " + str(number) + " canvasses")
	return canvasses
