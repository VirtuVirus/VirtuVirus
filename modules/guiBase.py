# External Imports
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
from PIL import Image, ImageTk

# Internal Imports
from modules import defaultConfigVars
from modules import guiUtils
from modules import utilities
from modules import sharedData
from modules import agents
from modules import simulation
from modules import graph

# Dev Vars
enableDebugButtons = False

# Path
import sys, os
if getattr(sys, 'frozen', False):
	application_path = sys._MEIPASS
	application_path = application_path + "/"
elif __file__:
	application_path = os.path.dirname(__file__)
	application_path = os.path.abspath(os.path.join(application_path, os.pardir))
	application_path = application_path + "/"

def defineGUI():
	try:
		root = tk.Tk()
	except Exception as error:
		if "linux" in sys.platform and "wayland" in error.__str__():
			print("An error occured while initializing VirtuVirus.")
			print("Your terminal seems to be incompatible with running Tkinter in the Wayland backend.")
			print("Please try using a different terminal.")
			exit(1)
		else:
			print("An error occured while initializing VirtuVirus. Is Tkinter functional on your system ?")
			exit(1)
	root.title("VirtuVirus")
	root.iconname("VirtuVirus")
	root.minsize(defaultConfigVars.WIDTH, defaultConfigVars.HEIGHT)
	root.wm_iconname("VirtuVirus")
	root.wm_title("VirtuVirus")

	# Set icon
	if "win" in sys.platform and not "darwin" in sys.platform:
		try:
			root.wm_iconbitmap(default=application_path+"assets/icon.ico")
		except:
			print("An error occured while setting the icon.")
	else:
		img = tk.PhotoImage(file=application_path+'assets/icon.png')
		root.tk.call('wm', 'iconphoto', root._w, img)

	# and theme
	style = ttk.Style(root)
	if "win" in sys.platform:
		style.theme_use('vista')
	else:
		style.theme_use('clam')

	# Create frame at the top
	topZone = guiUtils.createFrame(root, tk.TOP, fill="both", expand=True)

	# Create the zone for spawning canvass
	canvasZone = guiUtils.createFrame(topZone, tk.RIGHT, fill="both", expand=True)

	# Insert an empty placeholder in the zone for the canvass
	backgroundCanvas = tk.Canvas(canvasZone, bg="grey")
	backgroundCanvas.pack(fill="both", expand=True)

	# On the left of the zone for canvass, add zones for control of the simulation and the agents and the settings
	controlZone = guiUtils.createFrame(topZone, tk.LEFT)

	# Add VirtuVirus Logo on top
	logoFile = Image.open(application_path+"assets/icon.png")
	logoFile = logoFile.resize((int(defaultConfigVars.WIDTH/5.2), int(defaultConfigVars.HEIGHT/4)), Image.ANTIALIAS)
	logoFile = ImageTk.PhotoImage(logoFile)
	logoLabel = tk.Label(controlZone, image=logoFile)
	logoLabel.image = logoFile
	logoLabel.pack(side=tk.TOP)

	# Add VirtuVirus Label on top
	virtuVirusLabel = ttk.Label(controlZone, text="VirtuVirus", font=("Helvetica", 20))
	virtuVirusLabel.pack(side=tk.TOP, pady=(0, 20))

	# Create the zone for the control of the simulation
	simulationControlZone = guiUtils.createFrame(controlZone, tk.TOP, padding=(5, 5, 5, 5), ipady=10)

	# Create the zone for the control of the agents
	agentsControlZone = guiUtils.createFrame(controlZone, tk.TOP, padding=(5, 5, 5, 5))

	# Add the respective labels
	ttk.Label(simulationControlZone, text="Simulation", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)

	# Create start, stop and pause buttons with icons
	StartAndStopZone = guiUtils.createFrame(simulationControlZone, tk.TOP)
	StartSimulationButton = ttk.Button(StartAndStopZone, text="Start", padding=(2, 2, 2, 2),command=lambda: checkIfReadyThenStart())
	StartSimulationButton.pack(side=tk.LEFT)
	StopSimulationButton = ttk.Button(StartAndStopZone, text="Stop", padding=(2, 2, 2, 2), command=lambda: stopSimulation(), state=tk.DISABLED)
	StopSimulationButton.pack(side=tk.RIGHT)
	PauseSimulationButton = ttk.Button(simulationControlZone, text="Pause Simulation", command=lambda: pauseOrResumeSimulation(),padding=(2, 2, 2, 2), state=tk.DISABLED)
	PauseSimulationButton.pack(side=tk.TOP)
	ClearSimulationButton = ttk.Button(simulationControlZone, text="Clear Simulation", command=lambda: clearSimulations(), padding=(2, 2, 2, 2))
	ClearSimulationButton.pack(side=tk.TOP)
	
	OpenSettingsButton = ttk.Button(simulationControlZone, text="Modify Settings", padding=(2, 2, 2, 2), command=lambda: defineSettingsDialogBox(root))
	OpenSettingsButton.pack(side=tk.TOP)
	ShowCurrentGraph = ttk.Button(simulationControlZone, text="Show Graph", command=lambda: showGraphSelectWindow(root), padding=(2, 2, 2, 2), state=tk.DISABLED)
	ShowCurrentGraph.pack(side=tk.TOP)

	if enableDebugButtons == True:
		PrintGlobalVariablesButton = ttk.Button(simulationControlZone, text="Print Global Variables", padding=(2, 2, 2, 2), command=lambda: print(sharedData.getAllGlobalVars()))
		PrintGlobalVariablesButton.pack(side=tk.TOP)


	# Create the zone for the control of the agents
	ttk.Label(agentsControlZone, text="Agents", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)
	# Have count for each type of agent
	AgentCountZone = guiUtils.createFrame(agentsControlZone, tk.LEFT)
	SaneCountLabel = ttk.Label(AgentCountZone, text="Sane : 0")
	SaneCountLabel.pack(side=tk.TOP)
	InfectedCountLabel = ttk.Label(AgentCountZone, text="Infected : 0")
	InfectedCountLabel.pack(side=tk.TOP)
	ImmuneCountLabel = ttk.Label(AgentCountZone, text="Immune : 0")
	ImmuneCountLabel.pack(side=tk.TOP)
	DeadCountLabel = ttk.Label(AgentCountZone, text="Dead : 0")
	DeadCountLabel.pack(side=tk.TOP)

	# Create area for status on the bottom
	statusZone = guiUtils.createFrame(root, tk.BOTTOM, padding=(5, 5, 5, 5), fill="x")
	statusLabel = ttk.Label(statusZone, text="No simulation zone has been spawned.", padding=(10, 0, 0, 0))
	statusLabel.pack(side=tk.LEFT)
	timeLabel = ttk.Label(statusZone, text="Time has not been initiated.", padding=(0, 0, 5, 0))
	timeLabel.pack(side=tk.RIGHT)

	return {"mainWindowRoot": root, "simulationZone": backgroundCanvas, "interactiveButtons": {"startButton": StartSimulationButton, "stopButton": StopSimulationButton, "pauseButton": PauseSimulationButton, "clearButton": ClearSimulationButton, "showGraphButton": ShowCurrentGraph, "openSettingsButton": OpenSettingsButton}, "counters":{"saneCount": SaneCountLabel, "infectedCount": InfectedCountLabel, "immuneCount": ImmuneCountLabel, "deadCount": DeadCountLabel}, "statusLabel": statusLabel, "timeLabel": timeLabel}

def defineSettingsDialogBox(window_root):
	settingsDialogBox = tk.Toplevel()
	settingsDialogBox.title("Simulation Setup")
	settingsDialogBox.iconname("Simulation Setup")
	settingsDialogBox.resizable(False, False)
	settingsDialogBox.wm_iconname("Simulation Setup")
	settingsDialogBox.wm_title("Simulation Setup")

	# Lock main window
	settingsDialogBox.grab_set()
	settingsDialogBox.wm_transient(window_root)

	# Set icon
	if "win" in sys.platform and not "darwin" in sys.platform:
		try:
			settingsDialogBox.wm_iconbitmap(default=application_path+"assets/icon.ico")
		except:
			print("An error occured while setting the icon.")
	else:
		img = tk.PhotoImage(file=application_path+'assets/icon.png')
		settingsDialogBox.tk.call('wm', 'iconphoto', settingsDialogBox._w, img)
	
	mainSettingsFrame = guiUtils.createFrame(settingsDialogBox, tk.TOP, fill="both", expand=True)

	# Simulation
	simulationSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(simulationSettingsFrame, text="Simulation", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)

	NumberOfSimulationsFrame = guiUtils.createFrame(simulationSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(NumberOfSimulationsFrame, text="Number of simulations (1-15) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	simulationCountEntry = ttk.Entry(NumberOfSimulationsFrame, width=3)
	simulationCountEntry.pack(side=tk.RIGHT)
	simulationCountEntry.insert(0, "4")

	framerateFrame = guiUtils.createFrame(simulationSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(framerateFrame, text="Framerate : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	framerateEntry = ttk.Entry(framerateFrame, width=3)
	framerateEntry.pack(side=tk.RIGHT)
	framerateEntry.insert(0, "24")

	sizeFrame = guiUtils.createFrame(simulationSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(sizeFrame, text="Size (300 max) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	sizeEntryWidth = ttk.Entry(sizeFrame, width=4)
	sizeEntryWidth.pack(side=tk.RIGHT)
	sizeEntryWidth.insert(0, "300")
	ttk.Label(sizeFrame, text="x", padding=(5, 5, 5, 5)).pack(side=tk.RIGHT)
	sizeEntryHeight = ttk.Entry(sizeFrame, width=4)
	sizeEntryHeight.pack(side=tk.RIGHT)
	sizeEntryHeight.insert(0, "300")

	makeLastSimulationQuarantineFrame = guiUtils.createFrame(simulationSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(makeLastSimulationQuarantineFrame, text="Make last simulation quarantine :", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	makeLastSimulationQuarantineCheckbox = ttk.Checkbutton(makeLastSimulationQuarantineFrame, variable=tk.IntVar())
	makeLastSimulationQuarantineCheckbox.pack(side=tk.RIGHT)
	makeLastSimulationQuarantineCheckbox.state(["selected"])

	# Agents
	agentSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(agentSettingsFrame, text="Agents", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)

	numberOfSaneAgentsFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(numberOfSaneAgentsFrame, text="Sane agents per simulation : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	saneAgentCountEntry = ttk.Entry(numberOfSaneAgentsFrame, width=4)
	saneAgentCountEntry.pack(side=tk.RIGHT)
	saneAgentCountEntry.insert(0, "99")

	numberOfInfectedAgentsFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(numberOfInfectedAgentsFrame, text="Infected agents per simulation : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	infectedAgentCountEntry = ttk.Entry(numberOfInfectedAgentsFrame, width=3)
	infectedAgentCountEntry.pack(side=tk.RIGHT)
	infectedAgentCountEntry.insert(0, "1")

	numberOfImmuneAgentsFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(numberOfImmuneAgentsFrame, text="Immune agents per simulation : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	immuneAgentCountEntry = ttk.Entry(numberOfImmuneAgentsFrame, width=3)
	immuneAgentCountEntry.pack(side=tk.RIGHT)
	immuneAgentCountEntry.insert(0, "0")

	maximumSpeedFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(maximumSpeedFrame, text="Maximum agent speed (pixels/s) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	maximumSpeedEntry = ttk.Entry(maximumSpeedFrame, width=3)
	maximumSpeedEntry.pack(side=tk.RIGHT)
	maximumSpeedEntry.insert(0, "48")

	agentSizeFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(agentSizeFrame, text="Agent size (pixels) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)	
	agentSizeEntry = ttk.Entry(agentSizeFrame, width=3)
	agentSizeEntry.pack(side=tk.RIGHT)
	agentSizeEntry.insert(0, "10")

	enableSymptomlessAgentsFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(enableSymptomlessAgentsFrame, text="Enable symtomless agents :", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	enableSymptomlessAgentsCheckbox = ttk.Checkbutton(enableSymptomlessAgentsFrame, variable=tk.IntVar())
	enableSymptomlessAgentsCheckbox.pack(side=tk.RIGHT)
	enableSymptomlessAgentsCheckbox.state(["selected"])

	symptomlessAgentsChanceFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(symptomlessAgentsChanceFrame, text="Chance of symptomless agents (0-100) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	symptomlessAgentsChanceEntry = ttk.Entry(symptomlessAgentsChanceFrame, width=3)
	symptomlessAgentsChanceEntry.pack(side=tk.RIGHT)
	symptomlessAgentsChanceEntry.insert(0, "3")

	# Agents behavior
	agentBehaviorSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(agentBehaviorSettingsFrame, text="Behaviors", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)

	enableCentralTravelFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(enableCentralTravelFrame, text="Enable central travel :", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	enableCentralTravelCheckbox = ttk.Checkbutton(enableCentralTravelFrame, variable=tk.IntVar())
	enableCentralTravelCheckbox.pack(side=tk.RIGHT)
	enableCentralTravelCheckbox.state(["selected"])  # Solution for ttk not having select() function.

	centralBehaviorChanceFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(centralBehaviorChanceFrame, text="Central travel chance (0-100) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	centralBehaviorChanceEntry = ttk.Entry(centralBehaviorChanceFrame, width=3)
	centralBehaviorChanceEntry.pack(side=tk.RIGHT)
	centralBehaviorChanceEntry.insert(0, "5")

	obviousCentralTravelFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(obviousCentralTravelFrame, text="Make central travel obvious : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	obviousCentralTravelCheckbox = ttk.Checkbutton(obviousCentralTravelFrame, variable=tk.IntVar())
	obviousCentralTravelCheckbox.pack(side=tk.RIGHT)

	centerRangeFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(centerRangeFrame, text="Center range (pixels) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	centerRangeEntry = ttk.Entry(centerRangeFrame, width=3)
	centerRangeEntry.pack(side=tk.RIGHT)
	centerRangeEntry.insert(0, "30")

	enableHumanLogicFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(enableHumanLogicFrame, text="Enable human logic :", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	enableHumanLogicCheckbox = ttk.Checkbutton(enableHumanLogicFrame, variable=tk.IntVar())
	enableHumanLogicCheckbox.pack(side=tk.RIGHT)
	enableHumanLogicCheckbox.state(["selected"])

	quarantineTimerLimitFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(quarantineTimerLimitFrame, text="Time before quarantine isolation (seconds) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	quarantineTimerLimitEntry = ttk.Entry(quarantineTimerLimitFrame, width=2)
	quarantineTimerLimitEntry.pack(side=tk.RIGHT)
	quarantineTimerLimitEntry.insert(0, "3")

	# Virus
	virusSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(virusSettingsFrame, text="Virus", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)

	infectiveRangeFrame = guiUtils.createFrame(virusSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(infectiveRangeFrame, text="Infective range : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	infectiveRangeEntry = ttk.Entry(infectiveRangeFrame, width=2)
	infectiveRangeEntry.pack(side=tk.RIGHT)
	infectiveRangeEntry.insert(0, "4")

	infectionChanceFrame = guiUtils.createFrame(virusSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(infectionChanceFrame, text="Infection risk per second (0-100) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	infectionChanceEntry = ttk.Entry(infectionChanceFrame, width=3)
	infectionChanceEntry.pack(side=tk.RIGHT)
	infectionChanceEntry.insert(0, "48")

	defaultRecoveryChanceFrame = guiUtils.createFrame(virusSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(defaultRecoveryChanceFrame, text="Default recovery chance per second (0-100)/10 :", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	defaultRecoveryChanceEntry = ttk.Entry(defaultRecoveryChanceFrame, width=3)
	defaultRecoveryChanceEntry.pack(side=tk.RIGHT)
	defaultRecoveryChanceEntry.insert(0, "24")

	recoveryChanceProgressFrame = guiUtils.createFrame(virusSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(recoveryChanceProgressFrame, text="Recovery chance progress per second (0-100)/1000 : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	recoveryChanceProgressEntry = ttk.Entry(recoveryChanceProgressFrame, width=3)
	recoveryChanceProgressEntry.pack(side=tk.RIGHT)
	recoveryChanceProgressEntry.insert(0, "36")

	deathRiskFrame = guiUtils.createFrame(virusSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(deathRiskFrame, text="Death risk per second (0-100)/10 : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	deathRiskEntry = ttk.Entry(deathRiskFrame, width=3)
	deathRiskEntry.pack(side=tk.RIGHT)
	deathRiskEntry.insert(0, "18")

	# When settings are modified, regenerate the config
	def generateConfigFromEntries():
		config = {}

		# We get the config from the entries
		config["simulationQuantity"] = int(simulationCountEntry.get())
		config["framerate"] = int(framerateEntry.get())
		config["canvasWidth"] = int(sizeEntryWidth.get())
		config["canvasHeight"] = int(sizeEntryHeight.get())
		config["isLastSimulationQuarantine"] = utilities.isChecked(makeLastSimulationQuarantineCheckbox)
		config["quarantineTimerLimit"] = int(quarantineTimerLimitEntry.get())
		config["numberOfSaneAgents"] = int(saneAgentCountEntry.get())
		config["numberOfInfectedAgents"] = int(infectedAgentCountEntry.get())
		config["numberOfImmuneAgents"] = int(immuneAgentCountEntry.get())
		config["maximumAgentSpeed"] = int(maximumSpeedEntry.get())
		config["agentSize"] = int(agentSizeEntry.get())
		config["isCentralTravelEnabled"] = utilities.isChecked(enableCentralTravelCheckbox)
		config["centralTravelChance"] = int(centralBehaviorChanceEntry.get())
		config["centerRange"] = int(centerRangeEntry.get())
		config["makeCentralTravelObvious"] = utilities.isChecked(obviousCentralTravelCheckbox)
		config["isHumanLogicEnabled"] = utilities.isChecked(enableHumanLogicCheckbox)
		config["infectiveRange"] = int(infectiveRangeEntry.get())
		config["infectionRisk"] = int(infectionChanceEntry.get())
		config["defaultRecoveryChance"] = int(defaultRecoveryChanceEntry.get())
		config["recoveryChanceProgress"] = int(recoveryChanceProgressEntry.get())
		config["deathRisk"] = int(deathRiskEntry.get())
		config["enableSymptomlessAgents"] = utilities.isChecked(enableSymptomlessAgentsCheckbox)
		config["symptomlessAgentsChance"] = int(symptomlessAgentsChanceEntry.get())

		# We apply the limits
		config["simulationQuantity"] = min(max(config["simulationQuantity"], 1),15)
		config["canvasWidth"] = min(max(config["canvasWidth"], 1), 300)
		config["canvasHeight"] = min(max(config["canvasHeight"], 1), 300)
		config["centralTravelChance"] = min(max(config["centralTravelChance"], 0), 100)
		config["infectionRisk"] = min(max(config["infectionRisk"], 0), 100)
		config["defaultRecoveryChance"] = min(max(config["defaultRecoveryChance"], 0), 100)
		config["recoveryChanceProgress"] = min(max(config["recoveryChanceProgress"], 0), 100)
		config["deathRisk"] = min(max(config["deathRisk"], 0), 100)
		config["numberOfSaneAgents"] = max(config["numberOfSaneAgents"], 0)
		config["numberOfInfectedAgents"] = max(config["numberOfInfectedAgents"], 0)
		config["numberOfImmuneAgents"] = max(config["numberOfImmuneAgents"], 0)
		config["maximumAgentSpeed"] = max(config["maximumAgentSpeed"], 1)
		config["agentSize"] = max(config["agentSize"], 1)
		config["quarantineTimerLimit"] = max(config["quarantineTimerLimit"], 0)
		config["centerRange"] = max(config["centerRange"], 0)
		config["symptomlessAgentsChance"] = min(max(config["symptomlessAgentsChance"], 0), 100)

		# We apply the necessary tweaks
		config["centralTravelChance"] = config["centralTravelChance"] / 100
		config["infectionRisk"] = config["infectionRisk"] / 100
		config["defaultRecoveryChance"] = config["defaultRecoveryChance"] / 100 / 10
		config["recoveryChanceProgress"] = config["recoveryChanceProgress"] / 100 / 1000
		config["deathRisk"] = config["deathRisk"] / 100 / 10
		config["symptomlessAgentsChance"] = config["symptomlessAgentsChance"] / 100

		# We adapt to the framerate where necessary
		config["maximumAgentSpeed"] /= config["framerate"]
		config["centralTravelChance"] /= config["framerate"]
		config["infectionRisk"] /= config["framerate"]
		config["defaultRecoveryChance"] /= config["framerate"]
		config["recoveryChanceProgress"] /= config["framerate"]
		config["deathRisk"] /= config["framerate"]

		# We send the config to shared data module
		sharedData.setConfig(config)

		# Close the window
		settingsDialogBox.destroy()

		# Print a message
		print("Settings applied.")
		
		return config
	
	# Bottom frame
	bottomFrame = guiUtils.createFrame(settingsDialogBox, tk.BOTTOM, padding=(5, 5, 5, 5))
	ttk.Button(bottomFrame, text="Spawn", command=lambda: spawnSimulations(generateConfigFromEntries()), padding=(2, 2, 2, 2)).pack(side=tk.LEFT)
	ttk.Button(bottomFrame, text="Cancel", command=settingsDialogBox.destroy, padding=(2, 2, 2, 2)).pack(side=tk.RIGHT)

def spawnSimulations(settings):
	guiUtils.clearCanvasses(sharedData.getGlobalVar("interactiveGraphicalComponents")["simulationZone"], sharedData.getGlobalVar("interactiveGraphicalComponents")["mainWindowRoot"])

	# We modify some buttons.
	buttons = sharedData.getGlobalVar("interactiveGraphicalComponents")["interactiveButtons"]
	buttons["startButton"].config(state=tk.NORMAL)
	buttons["pauseButton"].config(state=tk.DISABLED)
	buttons["stopButton"].config(state=tk.DISABLED)
	buttons["showGraphButton"].config(state=tk.DISABLED)

	guiUtils.generateCanvasses(sharedData.getGlobalVar("interactiveGraphicalComponents")["simulationZone"], settings["simulationQuantity"], settings["canvasWidth"], settings["canvasHeight"], sharedData.getGlobalVar("interactiveGraphicalComponents")["mainWindowRoot"], settings["isLastSimulationQuarantine"])
	agents.createAgents(sharedData.getGlobalVar("simulations"), sharedData.getVarInConfig("numberOfSaneAgents"), sharedData.getVarInConfig("numberOfInfectedAgents"), sharedData.getVarInConfig("numberOfImmuneAgents"))

	# Update all counts (we're right at the start of the simulation, so this method is acceptable)
	match settings["isLastSimulationQuarantine"]:
		case True:
			numberOfSaneAgents = sharedData.getVarInConfig("numberOfSaneAgents")*(settings["simulationQuantity"] - 1)
			numberOfInfectedAgents = sharedData.getVarInConfig("numberOfInfectedAgents")*(settings["simulationQuantity"] - 1)
			numberOfImmuneAgents = sharedData.getVarInConfig("numberOfImmuneAgents")*(settings["simulationQuantity"] - 1)
		case False:
			numberOfSaneAgents = sharedData.getVarInConfig("numberOfSaneAgents")*settings["simulationQuantity"]
			numberOfInfectedAgents = sharedData.getVarInConfig("numberOfInfectedAgents")*settings["simulationQuantity"]
			numberOfImmuneAgents = sharedData.getVarInConfig("numberOfImmuneAgents")*settings["simulationQuantity"]
	guiUtils.updateCounts(numberOfSaneAgents, numberOfInfectedAgents, numberOfImmuneAgents, 0)

	# And we indicate that the simulation is ready, but not started.
	sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="The simulation has not been started.")
	sharedData.getGlobalVar("interactiveGraphicalComponents")["timeLabel"].config(text="Waiting for simulation to start...")

def clearSimulations():
	guiUtils.clearCanvasses(sharedData.getGlobalVar("interactiveGraphicalComponents")["simulationZone"], sharedData.getGlobalVar("interactiveGraphicalComponents")["mainWindowRoot"])

	# We modify some buttons.
	buttons = sharedData.getGlobalVar("interactiveGraphicalComponents")["interactiveButtons"]
	buttons["startButton"].config(state=tk.NORMAL)
	buttons["pauseButton"].config(state=tk.DISABLED)
	buttons["stopButton"].config(state=tk.DISABLED)
	buttons["showGraphButton"].config(state=tk.DISABLED)

	# We reset the status label to its original message
	sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="No simulation zone has been spawned.")
	sharedData.getGlobalVar("interactiveGraphicalComponents")["timeLabel"].config(text="Time has not been initiated.")

def checkIfReadyThenStart():
	if sharedData.getGlobalVar("simulations") is not None:
		print("Starting simulation...")

		buttons = sharedData.getGlobalVar("interactiveGraphicalComponents")["interactiveButtons"]
		buttons["startButton"].config(state=tk.DISABLED)
		buttons["openSettingsButton"].config(state=tk.DISABLED)
		buttons["clearButton"].config(state=tk.DISABLED)
		buttons["pauseButton"].config(state=tk.NORMAL)
		buttons["stopButton"].config(state=tk.NORMAL)
		buttons["showGraphButton"].config(state=tk.NORMAL)

		sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="Attempting to start the simulation...")
		sharedData.getGlobalVar("interactiveGraphicalComponents")["timeLabel"].config(text="Initiating time...")

		simulation.startSimulation(sharedData.getGlobalVar("simulations"))
	else:
		tkmb.showwarning("Warning",'No simulation zone has been spawned. Use the "Modify Settings" button to spawn them.')

def stopSimulation():
	print("Stopping simulation...")

	buttons = sharedData.getGlobalVar("interactiveGraphicalComponents")["interactiveButtons"]
	buttons["startButton"].config(state=tk.DISABLED)
	buttons["openSettingsButton"].config(state=tk.NORMAL)
	buttons["clearButton"].config(state=tk.NORMAL)
	buttons["pauseButton"].config(state=tk.DISABLED)
	buttons["stopButton"].config(state=tk.DISABLED)
	buttons["showGraphButton"].config(state=tk.NORMAL)

	sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="Attempting to stop simulation...")

	simulation.stopSimulation(sharedData.getGlobalVar("simulations"))

def pauseOrResumeSimulation():
	if sharedData.getGlobalVar("isSimulationPaused") == False:
		print("Pausing simulation...")
		sharedData.writeGlobalVar("isSimulationPaused", True)
		sharedData.getGlobalVar("interactiveGraphicalComponents")["interactiveButtons"]["pauseButton"].config(text="Resume Simulation")
		sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="Simulation is paused.")
	else:
		print("Resuming simulation...")
		sharedData.writeGlobalVar("isSimulationPaused", False)
		sharedData.getGlobalVar("interactiveGraphicalComponents")["interactiveButtons"]["pauseButton"].config(text="Pause Simulation")
		sharedData.getGlobalVar("interactiveGraphicalComponents")["statusLabel"].config(text="Simulation has resumed.")

def showGraphSelectWindow(window_root):
	# Pause simulation
	if sharedData.getGlobalVar("isSimulationPaused") == False and sharedData.getGlobalVar("isSimulationRunning") == True:
		pauseOrResumeSimulation()
	
	# Window
	graphSelectWindow = tk.Toplevel()
	graphSelectWindow.title("Graph Selection")
	graphSelectWindow.iconname("Graph Selection")
	graphSelectWindow.resizable(False, False)
	graphSelectWindow.wm_iconname("Graph Selection")
	graphSelectWindow.wm_title("Graph Selection")

	# Lock main window
	graphSelectWindow.grab_set()
	graphSelectWindow.wm_transient(window_root)

	# Set icon
	if "win" in sys.platform and not "darwin" in sys.platform:
		try:
			graphSelectWindow.wm_iconbitmap(default=application_path+"assets/icon.ico")
		except:
			print("An error occured while setting the icon.")
	else:
		img = tk.PhotoImage(file=application_path+'assets/icon.png')
		graphSelectWindow.tk.call('wm', 'iconphoto', graphSelectWindow._w, img)

	# Variables
	dataTypeVariable = tk.StringVar(value="total")
	graphTypeVariable = tk.StringVar(value="line")
	timeFormatVariable = tk.StringVar(value="frames")
	simulations = sharedData.getGlobalVar("simulations")
	
	# GUI
	mainGraphSelectFrame = guiUtils.createFrame(graphSelectWindow, tk.TOP, fill="both", expand=True)

	dataTypeFrame = guiUtils.createFrame(mainGraphSelectFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(dataTypeFrame, text="Data Type", font=("Helvetica", 10, "bold"), padding=(5, 5, 5, 5)).pack(side = tk.TOP, anchor = tk.N)
	ttk.Radiobutton(dataTypeFrame, text="Total", variable=dataTypeVariable, value="total").pack(anchor = tk.W)
	ttk.Radiobutton(dataTypeFrame, text="Mean", variable=dataTypeVariable, value="mean").pack(anchor = tk.W)

	graphTypeSelectionFrame = guiUtils.createFrame(mainGraphSelectFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(graphTypeSelectionFrame, text="Graph Type", font=("Helvetica", 10, "bold"), padding=(5, 5, 5, 5)).pack(side = tk.TOP, anchor = tk.N)
	ttk.Radiobutton(graphTypeSelectionFrame, text="Lines", variable=graphTypeVariable, value="line").pack(anchor = tk.W)
	ttk.Radiobutton(graphTypeSelectionFrame, text="Bars (heavy)", variable=graphTypeVariable, value="bar").pack(anchor = tk.W)
	ttk.Radiobutton(graphTypeSelectionFrame, text="Sums", variable=graphTypeVariable, value="sum").pack(anchor = tk.W)

	simulationSelectionFrame = guiUtils.createFrame(mainGraphSelectFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	simulationSelectionFrame.pack(side = tk.LEFT)
	ttk.Label(simulationSelectionFrame, text="Simulations", font=("Helvetica", 10, "bold"), padding=(5, 5, 5, 5)).pack(side = tk.TOP, anchor = tk.N)
	# That sad moment when you discover that ttk has no support for listboxes.
	simulationSelectionList = tk.Listbox(simulationSelectionFrame, selectmode=tk.MULTIPLE, height=5, width=15)
	simulationSelectionList.pack(side = tk.LEFT, anchor = tk.N, expand=True, fill=tk.Y)
	for i in range(1,len(simulations)+1):
		if simulations[i-1]["isQuarantine"] == True:
			simulationSelectionList.insert("end", "Quarantine")
		else:
			simulationSelectionList.insert("end", "Simulation "+str(i))
	# ttk is being annoying today... The scrollbar's appearance is too big on Linux because of the clam theme. Still, it works just fine.
	scrollBar = ttk.Scrollbar(simulationSelectionFrame, orient=tk.VERTICAL, command=simulationSelectionList.yview)
	scrollBar.pack(side=tk.RIGHT, anchor = tk.N, fill=tk.Y)
	simulationSelectionList['yscrollcommand'] = scrollBar.set

	agentSelectionFrame = guiUtils.createFrame(mainGraphSelectFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(agentSelectionFrame, text="Agents", font=("Helvetica", 10, "bold"), padding=(5, 5, 5, 5)).pack(side = tk.TOP, anchor = tk.N)

	saneCheckboxFrame = guiUtils.createFrame(agentSelectionFrame, tk.TOP, anchor = tk.W)
	ttk.Label(saneCheckboxFrame, text="Sane : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT, anchor = tk.N)
	saneCheckbox = ttk.Checkbutton(saneCheckboxFrame, variable=tk.IntVar())
	saneCheckbox.pack(side=tk.RIGHT)
	saneCheckbox.state(["selected"])

	infectedCheckboxFrame = guiUtils.createFrame(agentSelectionFrame, tk.TOP, anchor = tk.W)
	ttk.Label(infectedCheckboxFrame, text="Infected : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT, anchor = tk.N)
	infectedCheckbox = ttk.Checkbutton(infectedCheckboxFrame, variable=tk.IntVar())
	infectedCheckbox.pack(side=tk.RIGHT)
	infectedCheckbox.state(["selected"])

	immuneCheckboxFrame = guiUtils.createFrame(agentSelectionFrame, tk.TOP, anchor = tk.W)
	ttk.Label(immuneCheckboxFrame, text="Immune : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT, anchor = tk.N)
	immuneCheckbox = ttk.Checkbutton(immuneCheckboxFrame, variable=tk.IntVar())
	immuneCheckbox.pack(side=tk.RIGHT)
	immuneCheckbox.state(["selected"])

	deadCheckboxFrame = guiUtils.createFrame(agentSelectionFrame, tk.TOP, anchor = tk.W)
	ttk.Label(deadCheckboxFrame, text="Dead : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT, anchor = tk.N)
	deadCheckbox = ttk.Checkbutton(deadCheckboxFrame, variable=tk.IntVar())
	deadCheckbox.pack(side=tk.RIGHT)
	deadCheckbox.state(["selected"])

	timeFormatSelectionFrame = guiUtils.createFrame(mainGraphSelectFrame, tk.LEFT, padding=(5, 5, 5, 5), ipady=10, anchor = tk.N)
	ttk.Label(timeFormatSelectionFrame, text="Time Format", font=("Helvetica", 10, "bold"), padding=(5, 5, 5, 5)).pack(side = tk.TOP, anchor = tk.N)
	ttk.Radiobutton(timeFormatSelectionFrame, text="Frames", variable=timeFormatVariable, value="frames").pack(anchor = tk.W)
	ttk.Radiobutton(timeFormatSelectionFrame, text="Seconds (in-simulation)", variable=timeFormatVariable, value="seconds").pack(anchor = tk.W)

	def extractSelectedSimulations(simulationList):
		selectedSimulations = []
		for i in range(0, simulationList.size()):
			if simulationList.selection_includes(i):
				selectedSimulations.append(i)
		
		if selectedSimulations == []:
			tkmb.showerror("Error", "No simulations were selected.")
		return selectedSimulations

	bottomFrame = guiUtils.createFrame(graphSelectWindow, tk.BOTTOM, padding=(5, 5, 5, 5))
	ttk.Button(bottomFrame, text="Generate", command=lambda: graph.generateGraph(dataTypeVariable.get(), graphTypeVariable.get(), extractSelectedSimulations(simulationSelectionList), {"Sane" : utilities.isChecked(saneCheckbox), "Infected" : utilities.isChecked(infectedCheckbox), "Immune" : utilities.isChecked(immuneCheckbox), "Dead" : utilities.isChecked(deadCheckbox)}, timeFormatVariable.get()), padding=(2, 2, 2, 2)).pack(side=tk.LEFT)
	ttk.Button(bottomFrame, text="Close", command=graphSelectWindow.destroy, padding=(2, 2, 2, 2)).pack(side=tk.RIGHT)
