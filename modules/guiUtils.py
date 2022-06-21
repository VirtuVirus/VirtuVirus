# External Imports
import tkinter as tk
import tkinter.ttk as ttk

# Internal Imports
from modules import defaultConfigVars
from modules import sharedData

def createFrame(root, location, padding = (0, 0, 0, 0), fill = None, expand = None, anchor = None, ipadx = None, ipady = None):
	frame = ttk.Frame(root, padding=padding)
	frame.pack(side=location, fill = fill, expand = expand, anchor = anchor, ipadx = ipadx, ipady = ipady)
	return frame

def generateCanvasses(CanvasRoot, number, width, height, windowRoot, hasInfectiveContainer = False):
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
	
	if hasInfectiveContainer and number > 1:
		canvas.config(highlightthickness=2, highlightbackground="red")
		canvasses[-1]["isInfectiveContainer"] = True
		
	# Adapt minimal resolution of windowRoot
	windowRoot.minsize(int(width*min(5, number)+200), max(int(height*j+55), defaultConfigVars.HEIGHT))

	sharedData.writeGlobalVar("canvasses", canvasses)
	
	return canvasses

def clearCanvasses(canvasRoot, windowRoot):
	for canvas in canvasRoot.grid_slaves():
		canvas.destroy()

	# Change canvasRoot size back to zero
	canvasRoot.config(width=0, height=0)

	# We empty all the canvasses from the shared data.
	sharedData.writeGlobalVar("canvasses", None)
	
	windowRoot.minsize(defaultConfigVars.WIDTH, defaultConfigVars.HEIGHT)