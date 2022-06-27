# External Imports
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

	agent["type"] = None
	agent["infectionZone"] = None

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
	isCentralTravelEnabled = sharedData.getVarInConfig("isCentralTravelEnabled")
	isHumanLogicEnabled = sharedData.getVarInConfig("isHumanLogicEnabled")
	centralTravelChance = sharedData.getVarInConfig("centralTravelChance")
	centerRange = sharedData.getVarInConfig("centerRange")
	canvasWidth = sharedData.getVarInConfig("canvasWidth")
	canvasHeight = sharedData.getVarInConfig("canvasHeight")
	framerate = sharedData.getVarInConfig("framerate")

	# Generate random starter movement
	local_x_speed, local_y_speed = maxSpeed*random.random(), maxSpeed*random.random()
	if random.randint(0, 1) == 1:
		local_x_speed *= -1
	if random.randint(0, 1) == 1:
		local_y_speed *= -1

	time.sleep(0.5) # Doing that somehow prevents a problem where the agent doesn't move.

	while sharedData.getGlobalVar("isSimulationRunning") == True and agent["type"] != "Dead":
		# Prevent thread surviving
		if False or agent not in simulation["agents"] or agent["type"] == "Dead" or sharedData.getGlobalVar("isSimulationRunning") == False or len(simulation["connectedThreads"]) == 0:
			return

		# Central Travel
		if isCentralTravelEnabled == True:
			centralTravelChanceTest = random.random()

			if isHumanLogicEnabled == True:
				# If the agent is infected, we lower the chance.
				if agent["type"] == "Infected":
					centralTravelChanceTest *= 3
				# If there are lots of infected, we make the requirement more strict.
				if agent["type"] == "Sane":
					centralTravelChance *= (len(simulation["agents"]) - len(simulation["infectedAgents"])+len(simulation["deadAgents"])*3)/len(simulation["agents"])
			
			if centralTravelChanceTest <= centralTravelChance:
				(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent["2DModel"])
				(CenterX, CenterY) = utilities.get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)

				testCordX, testCordY = utilities.getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

				while sharedData.getGlobalVar("isSimulationRunning") == False and sqrt(testCordX**2 + testCordY**2) > centerRange:
					# Go to center
					local_x_speed, local_y_speed = (canvasWidth/2 - CenterX)/framerate, (canvasHeight/2 - CenterY)/framerate
					canvas.move(agent["2DModel"], local_x_speed, local_y_speed)

					(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent["2DModel"])
					(CenterX, CenterY) = utilities.get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
					testCordX, testCordY = utilities.getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

					if False or agent not in simulation["agents"] or agent["type"] == "Dead" or sharedData.getGlobalVar("isSimulationRunning") == False or len(simulation["connectedThreads"]) == 0:
						return
					time.sleep(1/framerate) # Needs syncing
				
				# Regenerate starter movement
				local_x_speed, local_y_speed = maxSpeed*random.random(), maxSpeed*random.random()
				if random.randint(0, 1) == 1:
					local_x_speed *= -1
				if random.randint(0, 1) == 1:
					local_y_speed *= -1
		# Make the agents bounce against the screen borders.
		canvas.move(agent["2DModel"], local_x_speed, local_y_speed)
		(leftPos, topPos, rightPos, bottomPos) = canvas.coords(agent["2DModel"])

		if leftPos <= 0 or rightPos >= canvasWidth:
			local_x_speed = -local_x_speed
		if topPos <= 0 or bottomPos >= canvasHeight:
			local_y_speed = -local_y_speed
		
		utilities.waitIfPaused()
		time.sleep(1/framerate) # Needs syncing
	return

def infectAgent(agent, simulation):
	canvas = simulation["simulationZone"]
	size = sharedData.getVarInConfig("agentSize")
	infectiveRange = sharedData.getVarInConfig("infectiveRange")
	infectionRisk = sharedData.getVarInConfig("infectionRisk")
	defaultRecoveryChance = sharedData.getVarInConfig("defaultRecoveryChance")
	defaultRecoveryChanceProgress = sharedData.getVarInConfig("recoveryChanceProgress")
	deathRisk = sharedData.getVarInConfig("deathRisk")
	doHumanLogic = sharedData.getVarInConfig("isHumanLogicEnabled")
	framerate = sharedData.getVarInConfig("framerate")

	if agent["type"] == "Dead" or agent["type"] == "Immune" or agent["infectionZone"] != None:
		time.sleep(1)
		if agent["type"] == "Dead" or agent["type"] == "Immune" or agent["infectionZone"] != None:
			return
	agent["type"] = "Infected"

	if agent not in simulation["infectedAgents"]:
		simulation["infectedAgents"].append(agent)
	if agent in simulation["saneAgents"]:
		simulation["saneAgents"].remove(agent)

	simulation["simulationZone"].itemconfig(agent["2DModel"], fill="red")

	# We create the infectious zone and append it.
	infectionZone = canvas.create_oval(0, 0, 0+(size*infectiveRange), 0+(size*infectiveRange))
	agent["infectionZone"] = infectionZone

	# We set the default Recovery chance progression
	localRecoveryChanceProgress = 0

	while sharedData.getGlobalVar("isSimulationRunning") == True and agent["type"] == "Infected":
		# Get cords of the agents and the agents' infectious zone.
		(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent["2DModel"])
		(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos) = canvas.coords(infectionZone)

		# Get center cords
		(AgentCenterX, AgentCenterY) = utilities.get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
		(InfectCenterX, InfectCenterY) = utilities.get2CenterCoordsFrom4Coords(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos)

		# Move agent_infectious_zone to the agent's position
		canvas.move(infectionZone, AgentCenterX-InfectCenterX, AgentCenterY-InfectCenterY)

		# Infect overlapping agents
		overlappingAgentModels = canvas.find_overlapping(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos)
		for overlappingAgentModel in overlappingAgentModels:
			if overlappingAgentModel != agent["2DModel"] and overlappingAgentModel != infectionZone:
				if random.random() < infectionRisk: # Give them a chance to escape unharmed.
					# We try and locate a sane agent that owns the model.
					for newAgent in simulation["saneAgents"]:
						if newAgent["2DModel"] == overlappingAgentModel and newAgent["type"] == "Sane":
							utilities.createThread(simulation["connectedThreads"], infectAgent, (newAgent,simulation))
		
		# Very low chance for the agent to be immunized, that progressively increases.
		if random.random() < defaultRecoveryChance + localRecoveryChanceProgress:
			canvas.delete(infectionZone)
			agent["infectionZone"] = None
			ImmunizeAgent(agent, simulation)
			return
		localRecoveryChanceProgress += defaultRecoveryChanceProgress

		# Low risk for the agent to die. If Human Logic is enabled, the risk gets higher with the number of infected people.
		if (random.random() < deathRisk - localRecoveryChanceProgress/4) or (random.random() < deathRisk * len(simulation["infectedAgents"])/(len(simulation["saneAgents"])+len(simulation["immuneAgents"])) - localRecoveryChanceProgress/4 and doHumanLogic == True):
			canvas.delete(infectionZone)
			agent["infectionZone"] = None
			KillAgent(agent, simulation)
			return
		
		utilities.waitIfPaused()
		time.sleep(1/framerate) # Needs syncing
	
	canvas.delete(infectionZone)
	agent["infectionZone"] = None
	return

def ImmunizeAgent(agent, simulation):
	if agent in simulation["deadAgents"]:
		return
	
	if agent not in simulation["immuneAgents"]:
		simulation["immuneAgents"].append(agent)
	else:
		return
	agent["type"] = "Immune"

	simulation["simulationZone"].itemconfig(agent["2DModel"], fill="green")

	if agent in simulation["saneAgents"]: #In case of bug
		simulation["saneAgents"].remove(agent)
	if agent in simulation["infectedAgents"]:
		simulation["infectedAgents"].remove(agent)

	return

def KillAgent(agent, simulation):
	if agent not in simulation["deadAgents"]:
		simulation["deadAgents"].append(agent)
	else:
		return
	agent["type"] = "Dead"

	simulation["simulationZone"].itemconfig(agent["2DModel"], fill="grey")
	simulation["simulationZone"].tag_lower(agent["2DModel"])

	if agent in simulation["saneAgents"]: #In case of bug
		simulation["saneAgents"].remove(agent)
	if agent in simulation["infectedAgents"]:
		simulation["infectedAgents"].remove(agent)
	
	return
