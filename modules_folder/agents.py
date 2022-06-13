# External Imports
from math import sqrt
from time import sleep
from random import randint, random

# Internal Imports
from modules_folder.utilities import createThread, get2CenterCoordsFrom4Coords, getCentralCenterCordsFromTopLeftCords
from modules_folder.gui_base import canvas
from modules_folder.global_vars import SimulationStopSignal, cureSignal, Agents, SaneAgents, ImmuneAgents, InfectedAgents, DeadAgents, InfectedZones, AgentMovementThreads, InfectionThreads
from modules_folder.config_vars import *

def createAgents(quantity, type):
	for i in range(quantity):
		createAgent(type)
		sleep(0.005) # This trick prevents the agents from all running their checks at the EXACT same time. Helps against lag.
	return

def createAgent(type):
	global size
	
	# Randomly place the agent.
	x_position, y_position = randint(0, WIDTH), randint(0, HEIGHT)

	agent = canvas.create_oval(x_position, y_position, x_position+size, y_position+size, fill="blue")
	Agents.append(agent)

	# We give it movement
	createThread(AgentMovementThreads, moveAgent, (agent,))

	if type == "Infected":
		createThread(InfectionThreads, infectAgent, (agent,))
	elif type == "Immune":
		ImmunizeAgent(agent)
	else:
		SaneAgents.append(agent)
	return agent

def ImmunizeAgent(agent):
	if agent in DeadAgents:
		return
	if agent not in ImmuneAgents:
		ImmuneAgents.append(agent)
	else:
		return

	canvas.itemconfig(agent, fill="green")

	if agent in InfectedAgents:
		InfectedAgents.remove(agent)
	return

def KillAgent(agent):
	if agent not in DeadAgents:
		DeadAgents.append(agent)
	else:
		return

	canvas.itemconfig(agent, fill="grey")
	canvas.tag_lower(agent)

	if agent in SaneAgents: #In case of bug
		SaneAgents.remove(agent)
	if agent in InfectedAgents:
		InfectedAgents.remove(agent)
	return

def infectAgent(agent):
	if agent in DeadAgents or agent in InfectedAgents:
		return

	canvas.itemconfig(agent, fill="red")

	# We create the infectious zone and append it.
	agent_infectious_zone = canvas.create_oval(0, 0, 0+(size*infective_range), 0+(size*infective_range), )
	InfectedZones.append(agent_infectious_zone)

	# We set the default Recovery chance progression
	localRecoveryChanceProgress = 0

	# We add the agent to the infected agents.
	if agent in SaneAgents:
		SaneAgents.remove(agent)
	if agent not in InfectedAgents:
		InfectedAgents.append(agent)

	while SimulationStopSignal == False:
		# Get cords of the agents and the agents' infectious zone.
		try:
			(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
			(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos) = canvas.coords(agent_infectious_zone)
		except:
			return

		# Get center cords
		(AgentCenterX, AgentCenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
		(InfectCenterX, InfectCenterY) = get2CenterCoordsFrom4Coords(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos)

		# Move agent_infectious_zone to the agent's position
		canvas.move(agent_infectious_zone, AgentCenterX-InfectCenterX, AgentCenterY-InfectCenterY)

		# Infect overlapping agents
		overlapping_agents = canvas.find_overlapping(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos)
		for overlapping_agent in overlapping_agents:
			if overlapping_agent != agent and overlapping_agent != agent_infectious_zone and overlapping_agent in SaneAgents:
				if random() < infectionChance: # Give them a chance to escape unharmed.
					createThread(InfectionThreads, infectAgent, (overlapping_agent,))
		
		# Very low chance for the agent to be immunized.
		if random() < defaultRecoveryChance + localRecoveryChanceProgress or cureSignal == True:
			ImmunizeAgent(agent)
			canvas.delete(agent_infectious_zone)
			return
		localRecoveryChanceProgress += defaultRecoveryChanceProgress

		# Low chance for the agent to die. If Human Behaviors are enabled, the chance gets higher with the number of infected people.
		try:
			if (random() < deathRisk - localRecoveryChanceProgress/4) or (random() < deathRisk * len(InfectedAgents)/(len(SaneAgents)+len(ImmuneAgents)) - localRecoveryChanceProgress/4 and doHumanBehaviors == True):
				KillAgent(agent)
				canvas.delete(agent_infectious_zone)
				return
		except:
			return

		if SimulationStopSignal:
			return
		sleep(frequency * 0.8)
	return

def moveAgent(agent):
	# Generate random starter movement
	local_x_speed, local_y_speed = maxXSpeed*random(), maxYSpeed*random()
	if randint(0, 1) == 1:
		local_x_speed *= -1
	if randint(0, 1) == 1:
		local_y_speed *= -1

	while SimulationStopSignal == False:
		# Prevent thread surviving
		if agent not in Agents or len(AgentMovementThreads) == 0 or agent in DeadAgents:
			return

		# Central Behavior
		from modules_folder.simulation import centralBehavior #Not the best solution, but that'll do for now.
		if centralBehavior == True:
			centralBehaviorChance = random()

			if doHumanBehaviors:
				# If the agent is infected, we make the chance lower.
				if agent in InfectedAgents:
					centralBehaviorChance *= 3
				# If there are lots of infected, we make the chance lower.
				if agent in SaneAgents:
					centralBehaviorChance /= (len(Agents) - len(InfectedAgents)+len(DeadAgents)*3)/len(Agents)
			
			if centralBehaviorChance <= centralBehaviorChanceRequirement:
				(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
				(CenterX, CenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)

				testCordX, testCordY = getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

				while SimulationStopSignal == False and centralBehavior == True and sqrt(testCordX**2 + testCordY**2) > centralBehaviorRange :
					# Go to center
					local_x_speed, local_y_speed = (WIDTH/2 - CenterX)/framerate, (HEIGHT/2 - CenterY)/framerate
					canvas.move(agent, local_x_speed, local_y_speed)

					try:
						(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
					except:
						return
					(CenterX, CenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
					testCordX, testCordY = getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

					if SimulationStopSignal or len(AgentMovementThreads) == 0 or agent in DeadAgents:
						return
					sleep(frequency)
				
				# Regenerate starter movement
				local_x_speed, local_y_speed = maxXSpeed*random(), maxYSpeed*random()
				if randint(0, 1) == 1:
					local_x_speed *= -1
				if randint(0, 1) == 1:
					local_y_speed *= -1
		# Make the agents bounce against the screen borders.
		canvas.move(agent, local_x_speed, local_y_speed)
		try:
			(leftPos, topPos, rightPos, bottomPos) = canvas.coords(agent)
		except:
			return

		if leftPos <= 0 or rightPos >= WIDTH:
			local_x_speed = -local_x_speed
		if topPos <= 0 or bottomPos >= HEIGHT:
			local_y_speed = -local_y_speed
		
		if SimulationStopSignal:
			return
		sleep(frequency)
	return