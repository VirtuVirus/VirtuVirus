# External Imports

# Internal Imports
from modules import sharedData
from modules import agents
from modules import utilities

def startSimulation(simulations):
	sharedData.writeGlobalVar("isSimulationRunning", True)

	# Here the time module will begin.

	for simulation in simulations:
		for agent in simulation["agents"]:
			if agent not in simulation["deadAgents"]: # Probably useless, considering no dead agent can be spawned at run time, but better safe than sorry.
				utilities.createThread(simulation["connectedThreads"], agents.moveAgent, (agent, simulation))
	
	print("Simulation started.")

	sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="A simulation is currently running.")