# External Imports
from time import sleep
from threading import Thread

# Internal Imports
from modules import sharedData
from modules import utilities
from modules import guiUtils

def clockThread():
	framerate = sharedData.getVarInConfig("framerate")

	frameTime = 0
	sharedData.writeGlobalVar("frameTime", frameTime)

	while sharedData.getGlobalVar("isSimulationRunning"):
		# Collect data for the counts.
		saneCount = utilities.getTotalCount("Sane")
		infectedCount = utilities.getTotalCount("Infected")
		deadCount = utilities.getTotalCount("Dead")
		immuneCount = utilities.getTotalCount("Immune")

		# Update the counts.
		guiUtils.updateCounts(saneCount, infectedCount, immuneCount, deadCount)

		# Update time
		sharedData.getGlobalVar("interactiveGraphicalComponents")["timeLabel"].config(text="Frames : " + str(frameTime) + " | Time (in-simulation) : " + str(int(frameTime/framerate)) + "s")

		sleep(1/framerate)
		frameTime += 1
		sharedData.writeGlobalVar("frameTime", frameTime)
