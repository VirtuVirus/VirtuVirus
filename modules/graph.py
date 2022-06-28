# External Imports
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Internal Imports
from modules import sharedData

def generateGraph(graphType):
	match graphType:
		case 'allTotalFrame':
			saneData = []
			infectedData = []
			immuneData = []
			deadData = []
			for count in sharedData.retrieveTotalCounts():
				saneData.append(count["Sane"])
				infectedData.append(count["Infected"])
				immuneData.append(count["Immune"])
				deadData.append(count["Dead"])
			
			plt.plot(saneData, label="Sane", color="blue")
			plt.plot(infectedData, label="Infected", color="red")
			plt.plot(immuneData, label="Immune", color="green")
			plt.plot(deadData, label="Dead", color="black")
			plt.legend()

			plt.xlabel("Frames")
			plt.ylabel("Population")
			plt.title("Agent population over time (in frames)")

			plt.show()
		
		case 'allMeanFrame':
			simulationCount = len(sharedData.getGlobalVar("simulations"))
			if sharedData.getVarInConfig("isLastSimulationQuarantine"):
				simulationCount -= 1

			saneData = []
			infectedData = []
			immuneData = []
			deadData = []
			for count in sharedData.retrieveTotalCounts():
				saneData.append(count["Sane"]/simulationCount)
				infectedData.append(count["Infected"])/simulationCount
				immuneData.append(count["Immune"]/simulationCount)
				deadData.append(count["Dead"]/simulationCount)
			
			plt.plot(saneData, label="Sane", color="blue")
			plt.plot(infectedData, label="Infected", color="red")
			plt.plot(immuneData, label="Immune", color="green")
			plt.plot(deadData, label="Dead", color="black")
			plt.legend()

			plt.xlabel("Frames")
			plt.ylabel("Mean of all populations")
			plt.title("Mean of the populations over time (in frames)")

			plt.show()

