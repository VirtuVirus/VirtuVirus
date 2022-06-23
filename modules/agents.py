# External Imports
import tkinter as tk
import tkinter.ttk as ttk
import random
import time
from math import sqrt

# Internal Imports
from modules import sharedData
from modules import utilities

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
	x_position, y_position = random.randint(0, width), random.randint(0, height)

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

def moveAgent(agent, simulation):
	maxSpeed = sharedData.getVarInConfig("maximumAgentSpeed")
	canvas = simulation["simulationZone"]

	# Generate random starter movement
	local_x_speed, local_y_speed = maxSpeed*random.random(), maxSpeed*random.random()
	if random.randint(0, 1) == 1:
		local_x_speed *= -1
	if random.randint(0, 1) == 1:
		local_y_speed *= -1

	time.sleep(0.5) # Doing that somehow prevents a problem where the agent doesn't move.

	while True:
		# Prevent thread surviving
		if False or agent not in simulation["agents"] or agent["type"] == "Dead" or sharedData.getGlobalVar("isSimulationRunning") == False or len(simulation["connectedThreads"]) == 0:
			return

		# Central Travel
		if sharedData.getVarInConfig("isCentralTravelEnabled"):
			centralBehaviorChance = random.random()

			if sharedData.getVarInConfig("isHumanLogicEnabled"):
				# If the agent is infected, we make the chance lower.
				if agent["type"] == "Infected":
					centralBehaviorChance *= 3
				# If there are lots of infected, we make the chance lower.
				if agent["type"] == "Sane":
					centralBehaviorChance /= (len(simulation["agents"]) - len(simulation["infectedAgents"])+len(simulation["deadAgents"])*3)/len(simulation["agents"])
			
			if centralBehaviorChance <= sharedData.getVarInConfig("centralBehaviorChance"):
				(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent["2DModel"])
				(CenterX, CenterY) = utilities.get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)

				testCordX, testCordY = utilities.getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

				while True and sqrt(testCordX**2 + testCordY**2) > sharedData.getVarInConfig("centerRange"):
					# Go to center
					local_x_speed, local_y_speed = (sharedData.getVarInConfig("canvasWidth")/2 - CenterX)/sharedData.getVarInConfig("framerate"), (sharedData.getVarInConfig("canvasHeight")/2 - CenterY)/sharedData.getVarInConfig("framerate")
					canvas.move(agent["2DModel"], local_x_speed, local_y_speed)

					(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent["2DModel"])
					(CenterX, CenterY) = utilities.get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
					testCordX, testCordY = utilities.getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

					if False or agent not in simulation["agents"] or agent["type"] == "Dead" or sharedData.getGlobalVar("isSimulationRunning") == False or len(simulation["connectedThreads"]) == 0:
						return
					time.sleep(1/sharedData.getVarInConfig("framerate"))
				
				# Regenerate starter movement
				local_x_speed, local_y_speed = maxSpeed*random.random(), maxSpeed*random.random()
				if random.randint(0, 1) == 1:
					local_x_speed *= -1
				if random.randint(0, 1) == 1:
					local_y_speed *= -1
		# Make the agents bounce against the screen borders.
		canvas.move(agent["2DModel"], local_x_speed, local_y_speed)
		(leftPos, topPos, rightPos, bottomPos) = canvas.coords(agent["2DModel"])

		if leftPos <= 0 or rightPos >= sharedData.getVarInConfig("canvasWidth"):
			local_x_speed = -local_x_speed
		if topPos <= 0 or bottomPos >= sharedData.getVarInConfig("canvasHeight"):
			local_y_speed = -local_y_speed
		
		if False:
			return
		
		time.sleep(1/sharedData.getVarInConfig("framerate"))
	return
