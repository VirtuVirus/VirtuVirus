# External Imports
import tkinter as tk
import tkinter.ttk as ttk
import random

# Internal Imports
from modules import sharedData

def createAgents(simulations, saneQuantity, infectedQuantity, immuneQuantity):
	for simulation in simulations:
		if simulation["isInfectiveContainer"] == False:
			for i in range(saneQuantity):
				createAgent(simulation, "Sane")
	
	for simulation in simulations:
		if simulation["isInfectiveContainer"] == False:
			for i in range(infectedQuantity):
				createAgent(simulation, "Infected")

	for simulation in simulations:
		if simulation["isInfectiveContainer"] == False:
			for i in range(immuneQuantity):
				createAgent(simulation, "Immune")

def createAgent(simulation, agentType):
	size = sharedData.getVarInConfig("agentSize")
	width = sharedData.getVarInConfig("canvasWidth")
	height = sharedData.getVarInConfig("canvasHeight")

	# Randomly place the agent.
	x_position, y_position = random.randint(10, width - 10), random.randint(10, height - 10)

	agent = {"2DModel": simulation["simulationZone"].create_oval(x_position, y_position, x_position+size, y_position+size, fill="blue")}
	simulation["agents"].append(agent)

	match agentType:
		case "Sane":
			simulation["simulationZone"].itemconfig(agent["2DModel"], fill="blue")
			agent["type"] = "Sane"
			simulation["saneAgents"].append(agent)
		case "Infected":
			simulation["simulationZone"].itemconfig(agent["2DModel"], fill="red")
			agent["type"] = "Infected"
			simulation["infectedAgents"].append(agent)
		case "Immune":
			simulation["simulationZone"].itemconfig(agent["2DModel"], fill="green")
			agent["type"] = "Immune"
			simulation["immuneAgents"].append(agent)

	return agent
