# External Imports
from threading import Thread
from time import sleep

# Internal Imports
from modules import defaultConfigVars
from modules import sharedData

def createThread(ThreadManagementArray, function, arguments=()):
	thread = Thread(target=function, args=arguments)
	thread.daemon = True
	thread.start()
	ThreadManagementArray.append(thread)
	return thread

def get2CenterCoordsFrom4Coords(leftPos, topPos, rightPos, bottomPos):
	return ((leftPos+rightPos)/2, (topPos+bottomPos)/2)

def getCentralCenterCordsFromTopLeftCords(CenterX, CenterY):
	return (CenterX - defaultConfigVars.WIDTH/2, CenterY - defaultConfigVars.HEIGHT/2)

def isChecked(checkbox):
	try:
		return checkbox.state()[0] == "selected" 
	except: 
		return False

def getTotalCount(agentType):
	simulations = sharedData.getGlobalVar("simulations")
	count = 0
	match agentType:
		case "Sane":
			for simulation in simulations:
				count += len(simulation["saneAgents"])
		case "Infected":
			for simulation in simulations:
				count += len(simulation["infectedAgents"])
		case "Dead":
			for simulation in simulations:
				count += len(simulation["deadAgents"])
		case "Immune":
			for simulation in simulations:
				count += len(simulation["immuneAgents"])

	return count

def waitIfPaused():
	while sharedData.getGlobalVar("isSimulationPaused"):
		sleep(1)
