# External Imports
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Internal Imports
from modules import sharedData

def generateGraph(dataType, graphType, selectedSimulations, selectedAgents, timeFormat):
	plt.close()

	if selectedSimulations == []:
		return
	
	saneData = []
	infectedData = []
	immuneData = []
	deadData = []
	
	data = sharedData.retrieveData()

	# We organize the data according to the selected method.
	if dataType == 'total' or dataType == 'mean':
		for frame in data:
			tempSane = 0
			tempInfected = 0
			tempImmune = 0
			tempDead = 0

			for simulationCount in frame:
				if simulationCount["Index"] in selectedSimulations:
					tempSane += simulationCount["Sane"]
					tempInfected += simulationCount["Infected"]
					tempImmune += simulationCount["Immune"]
					tempDead += simulationCount["Dead"]
			
			if dataType == "total":
				saneData.append(tempSane)
				infectedData.append(tempInfected)
				immuneData.append(tempImmune)
				deadData.append(tempDead)
			elif dataType == "mean":
				saneData.append(tempSane/len(selectedSimulations))
				infectedData.append(tempInfected/len(selectedSimulations))
				immuneData.append(tempImmune/len(selectedSimulations))
				deadData.append(tempDead/len(selectedSimulations))
	
	# If the time format is 'seconds', we need to convert the data to seconds.
	framerate = sharedData.getVarInConfig("framerate")
	if timeFormat == 'seconds':
		tempSaneData = []
		tempInfectedData = []
		tempImmuneData = []
		tempDeadData = []
		for i in range(0,len(saneData),framerate):
			tempSaneVar = 0
			tempInfectedVar = 0
			tempImmuneVar = 0
			tempDeadVar = 0
			try:
				altDivider = 0
				for j in range(i,i+framerate):
					tempSaneVar += saneData[j]/framerate
					tempInfectedVar += infectedData[j]/framerate
					tempImmuneVar += immuneData[j]/framerate
					tempDeadVar += deadData[j]/framerate
					altDivider += 1
			except IndexError:
				tempSaneVar *= framerate/altDivider
				tempInfectedVar *= framerate/altDivider
				tempImmuneVar *= framerate/altDivider
				tempDeadVar *= framerate/altDivider
			tempSaneData.append(tempSaneVar)
			tempInfectedData.append(tempInfectedVar)
			tempImmuneData.append(tempImmuneVar)
			tempDeadData.append(tempDeadVar)
		saneData = tempSaneData
		infectedData = tempInfectedData
		immuneData = tempImmuneData
		deadData = tempDeadData
	
	# We display it with the asked method.
	match graphType:
		case 'line':
			if selectedAgents["Sane"]:
				plt.plot(saneData, label="Sane", color="blue")
			if selectedAgents["Infected"]:
				plt.plot(infectedData, label="Infected", color="red")
			if selectedAgents["Immune"]:
				plt.plot(immuneData, label="Immune", color="green")
			if selectedAgents["Dead"]:
				plt.plot(deadData, label="Dead", color="black")
		case 'bar':
			if selectedAgents["Sane"]:
				plt.bar(range(len(saneData)), saneData, label="Sane", color="blue")
			if selectedAgents["Infected"]:
				plt.bar(range(len(infectedData)), infectedData, label="Infected", color="red")
			if selectedAgents["Immune"]:
				plt.bar(range(len(immuneData)), immuneData, label="Immune", color="green")
			if selectedAgents["Dead"]:
				plt.bar(range(len(deadData)), deadData, label="Dead", color="black")
		case 'sum':
			agents = []
			labels = []
			colors = []
			if selectedAgents["Sane"]:
				agents.append(saneData)
				labels.append("Sane")
				colors.append("blue")
			if selectedAgents["Infected"]:
				agents.append(infectedData)
				labels.append("Infected")
				colors.append("red")
			if selectedAgents["Immune"]:
				agents.append(immuneData)
				labels.append("Immune")
				colors.append("green")
			if selectedAgents["Dead"]:
				agents.append(deadData)
				labels.append("Dead")
				colors.append("black")

			plt.stackplot(range(len(saneData)), agents, labels=labels, colors=colors)
	plt.legend()

	match dataType:
		case 'total':
			plt.ylabel("Population")
			title = "Agent population"
		case 'mean':
			plt.ylabel("Mean of the agent populations")
			title = "Mean of the agent populations"
	
	match timeFormat:
		case 'frames':
			plt.xlabel("Frames")
			title += " over time (in frames)"
		case 'seconds':
			plt.xlabel("Seconds (in-simulation)")
			title += " over time (in simulation seconds)"

	plt.title(title)
	plt.show()
