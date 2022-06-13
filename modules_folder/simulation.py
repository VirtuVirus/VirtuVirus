# External Imports
from time import sleep

# Internal Imports
from modules_folder.config_vars import frequency
from modules_folder.global_vars import Agents, InfectedZones, SaneAgents, InfectedAgents, ImmuneAgents, DeadAgents, AgentMovementThreads, InfectionThreads, centralBehavior
from modules_folder.gui_base import canvas

def clearSimulation():
	stopSimulation()

	# Delete all the agents from the canvas
	for agent in Agents:
		canvas.delete(agent)
	for agent_infectious_zone in InfectedZones:
		canvas.delete(agent_infectious_zone)

	# Clear the lists.
	Agents.clear()
	SaneAgents.clear()
	InfectedAgents.clear()
	ImmuneAgents.clear()
	DeadAgents.clear()
	InfectedZones.clear()
	return

def stopSimulation():
	global SimulationStopSignal
	# Indicate that the simulation is stopping.
	SimulationStopSignal = True

	# Wait
	sleep(frequency*5)

	# Clear the threads
	AgentMovementThreads.clear()
	InfectionThreads.clear()
	
	SimulationStopSignal = False
	return

def ToggleCentralBehavior():
	global centralBehavior
	centralBehavior = not centralBehavior
	return