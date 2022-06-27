# External Imports

# Internal Imports
from modules import sharedData
from modules import agents
from modules import utilities
from modules import clock

clockThread = []

def startSimulation(simulations):
	sharedData.writeGlobalVar("isSimulationRunning", True)

	utilities.createThread(clockThread, clock.clockThread, ())

	for simulation in simulations:
		for agent in simulation["agents"]:
			if agent not in simulation["deadAgents"]: # Probably useless, considering no dead agent can be spawned at run time, but better safe than sorry.
				utilities.createThread(simulation["connectedThreads"], agents.moveAgent, (agent, simulation))
			if agent["type"] == "Infected":
				utilities.createThread(simulation["connectedThreads"], agents.infectAgent, (agent, simulation))
	
	
	print("Simulation started.")

	sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="A simulation is currently running.")

def stopSimulation(simulations):
	sharedData.writeGlobalVar("isSimulationRunning", False)

	# Here the time module will stop.

	print("Simulation stopped.")

	sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="The simulation has been stopped.")
