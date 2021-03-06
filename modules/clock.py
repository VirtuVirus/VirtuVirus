# External Imports
from time import sleep
from threading import Thread
import tkinter.messagebox as tkmb

# Internal Imports
from modules import sharedData
from modules import utilities
from modules import guiUtils
from modules import guiBase

def clockThread():
	framerate = sharedData.getVarInConfig("framerate")
	didAutomaticPause = False

	# We reset the frametime to 0.
	frameTime = 0
	sharedData.writeGlobalVar("frameTime", frameTime)

	# We reset the collected data.
	sharedData.resetData()

	while sharedData.getGlobalVar("isSimulationRunning"):
		# Collect data for the counts.
		saneCount = utilities.getTotalCount("Sane")
		infectedCount = utilities.getTotalCount("Infected")
		deadCount = utilities.getTotalCount("Dead")
		immuneCount = utilities.getTotalCount("Immune")

		# Update the counts.
		guiUtils.updateCounts(saneCount, infectedCount, immuneCount, deadCount)
		
		# Update the counts in the data collection.
		simulations = sharedData.getGlobalVar("simulations")
		tempSimulationList = []
		for indexOfSimulation in range(len(simulations)):
			numberOfSaneAgents = len(simulations[indexOfSimulation]["saneAgents"])
			numberOfInfectedAgents = len(simulations[indexOfSimulation]["infectedAgents"])
			numberOfImmuneAgents = len(simulations[indexOfSimulation]["immuneAgents"])
			numberOfDeadAgents = len(simulations[indexOfSimulation]["deadAgents"])
			tempSimulationList.append({"Index": indexOfSimulation, "Sane":numberOfSaneAgents, "Infected":numberOfInfectedAgents, "Immune":numberOfImmuneAgents, "Dead":numberOfDeadAgents})
		sharedData.addFrameCount(tempSimulationList)

		# Update time
		sharedData.getGlobalVar("interactiveGraphicalComponents")["timeLabel"].config(text="Frames : " + str(frameTime) + " | Time (in-simulation) : " + str(int(frameTime/framerate)) + "s")

		# If there are no more infected agents, automatically pause the simulation.
		if infectedCount <= 0 and didAutomaticPause == False and sharedData.getGlobalVar("isSimulationPaused") == False:
			guiBase.pauseOrResumeSimulation()
			didAutomaticPause = True
			tkmb.showinfo("Out of infected agents.", "There are no more infected agents. The simulation was automatically paused.")


		utilities.waitIfPaused()
		sleep(1/framerate)

		frameTime += 1
		sharedData.writeGlobalVar("frameTime", frameTime)
