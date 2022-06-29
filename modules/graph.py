# External Imports
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Internal Imports
from modules import sharedData

def oldGenerateGraph(graphType):
	plt.close()

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
				infectedData.append(count["Infected"]/simulationCount)
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

def generateGraph(dataType, graphType, selectedSimulations, selectedAgents, timeFormat):
	plt.close()

	if selectedSimulations == []:
		return
	
	if selectedAgents["Sane"]:
		saneData = []
	if selectedAgents["Infected"]:
		infectedData = []
	if selectedAgents["Immune"]:
		immuneData = []
	if selectedAgents["Dead"]:
		deadData = []
	
	data = sharedData.retrieveData()

	if dataType == 'total' or dataType == 'mean':
		for frame in data:
			tempSane = 0
			tempInfected = 0
			tempImmune = 0
			tempDead = 0

			for simulationCount in frame:
				if simulationCount["Index"] in selectedSimulations:
					if selectedAgents["Sane"]:
						tempSane += simulationCount["Sane"]
					if selectedAgents["Infected"]:
						tempInfected += simulationCount["Infected"]
					if selectedAgents["Immune"]:
						tempImmune += simulationCount["Immune"]
					if selectedAgents["Dead"]:
						tempDead += simulationCount["Dead"]
			
			if dataType == "total":
				if selectedAgents["Sane"]:
					saneData.append(tempSane)
				if selectedAgents["Infected"]:
					infectedData.append(tempInfected)
				if selectedAgents["Immune"]:
					immuneData.append(tempImmune)
				if selectedAgents["Dead"]:
					deadData.append(tempDead)
			elif dataType == "mean":
				if selectedAgents["Sane"]:
					saneData.append(tempSane/len(selectedSimulations))
				if selectedAgents["Infected"]:
					infectedData.append(tempInfected/len(selectedSimulations))
				if selectedAgents["Immune"]:
					immuneData.append(tempImmune/len(selectedSimulations))
				if selectedAgents["Dead"]:
					deadData.append(tempDead/len(selectedSimulations))
	
	if selectedAgents["Sane"]:
		plt.plot(saneData, label="Sane", color="blue")
	if selectedAgents["Infected"]:
		plt.plot(infectedData, label="Infected", color="red")
	if selectedAgents["Immune"]:
		plt.plot(immuneData, label="Immune", color="green")
	if selectedAgents["Dead"]:
		plt.plot(deadData, label="Dead", color="black")
	plt.legend()

	match dataType:
		case 'total':
			plt.ylabel("Population")
			title = "Agent population"
		case 'mean':
			plt.ylabel("Mean of all populations")
			title = "Mean of the populations"
	
	match timeFormat:
		case 'frames':
			plt.xlabel("Frames")
			title += " over time (in frames)"
		case 'seconds':
			plt.xlabel("Seconds (in-simulation)")
			title += " over time (in simulation seconds)"

	plt.title(title)
	plt.show()

