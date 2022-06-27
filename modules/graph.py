import matplotlib.pyplot as plt

from modules import sharedData

def generateGraph(graphType):
	match graphType:
		case 'allTotalFrame':
			saneData = []
			for count in sharedData.retrieveTotalCounts():
				saneData.append(count["Sane"])
			infectedData = []
			for count in sharedData.retrieveTotalCounts():
				infectedData.append(count["Infected"])
			immuneData = []
			for count in sharedData.retrieveTotalCounts():
				immuneData.append(count["Immune"])
			deadData = []
			for count in sharedData.retrieveTotalCounts():
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
			for count in sharedData.retrieveTotalCounts():
				saneData.append(count["Sane"]/simulationCount)
			infectedData = []
			for count in sharedData.retrieveTotalCounts():
				infectedData.append(count["Infected"]/simulationCount)
			immuneData = []
			for count in sharedData.retrieveTotalCounts():
				immuneData.append(count["Immune"]/simulationCount)
			deadData = []
			for count in sharedData.retrieveTotalCounts():
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

