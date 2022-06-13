from time import sleep

from modules_folder.config_vars import frequency
from modules_folder.global_vars import *

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