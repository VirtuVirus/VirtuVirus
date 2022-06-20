# External Imports
from ast import Pass
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
from sys import platform
from PIL import Image, ImageTk

# Internal Imports
from modules import defaultConfigVars
from modules import guiUtils

# Global variables
exampleCanvas = None

def defineGUI():
	global logo

	root = tk.Tk()
	root.title("VirtuVirus")
	root.iconname("VirtuVirus")
	root.minsize(defaultConfigVars.WIDTH, defaultConfigVars.HEIGHT)
	root.wm_iconname("VirtuVirus")


	# Set icon
	if "win" in platform:
		root.wm_iconbitmap(default="assets/icon.ico")
	else:
		img = tk.PhotoImage(file='assets/icon.png')
		root.tk.call('wm', 'iconphoto', root._w, img)

	# and theme
	style = ttk.Style(root)
	if "win" in platform:
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
	logoFile = Image.open("assets/icon.png")
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
	StartSimulationButton = ttk.Button(StartAndStopZone, text="Start", padding=(2, 2, 2, 2)).pack(side=tk.LEFT)
	StopSimulationButton = ttk.Button(StartAndStopZone, text="Stop", padding=(2, 2, 2, 2), state=tk.DISABLED).pack(side=tk.RIGHT)
	PauseSimulationButton = ttk.Button(simulationControlZone, text="Pause Simulation", padding=(2, 2, 2, 2), state=tk.DISABLED).pack(side=tk.TOP)
	
	OpenSettingsButton = ttk.Button(simulationControlZone, text="Modify Settings", padding=(2, 2, 2, 2), command=lambda: defineSettingsDialogBox(root)).pack(side=tk.TOP)
	ShowCurrentGraph = ttk.Button(simulationControlZone, text="Show Graph", padding=(2, 2, 2, 2), state=tk.DISABLED).pack(side=tk.TOP)


	# Create the zone for the control of the agents
	ttk.Label(agentsControlZone, text="Agents", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)
	# Have count for each type of agent
	AgentCountZone = guiUtils.createFrame(agentsControlZone, tk.LEFT)
	SaneCountLabel = ttk.Label(AgentCountZone, text="Sane : 0").pack(side=tk.TOP)
	InfectedCountLabel = ttk.Label(AgentCountZone, text="Infected : 0").pack(side=tk.TOP)
	ImmuneCountLabel = ttk.Label(AgentCountZone, text="Immune : 0").pack(side=tk.TOP)
	DeadCountLabel = ttk.Label(AgentCountZone, text="Dead : 0").pack(side=tk.TOP)


	# Create area for status on the bottom
	statusZone = guiUtils.createFrame(root, tk.BOTTOM, padding=(5, 5, 5, 5), fill="x")
	statusLabel = ttk.Label(statusZone, text="No simulation is currently running.", padding=(10, 0, 0, 0))
	statusLabel.pack(side=tk.LEFT)
	timeLabel = ttk.Label(statusZone, text="Time has not been initiated.", padding=(0, 0, 5, 0))
	timeLabel.pack(side=tk.RIGHT)

	return {"window_root": root, "simulation_zone": backgroundCanvas}

def defineSettingsDialogBox(window_root):
	settingsDialogBox = tk.Toplevel()
	settingsDialogBox.title("Simulation Setup")
	settingsDialogBox.iconname("Simulation Setup")
	#settingsDialogBox.minsize(700, 500)
	settingsDialogBox.resizable(False, False)
	settingsDialogBox.wm_iconname("Simulation Setup")

	# Lock main window
	settingsDialogBox.grab_set()
	settingsDialogBox.wm_transient(window_root)

	# Set icon
	if "win" in platform:
		settingsDialogBox.wm_iconbitmap(default="assets/icon.ico")
	else:
		img = tk.PhotoImage(file='assets/icon.png')
		settingsDialogBox.tk.call('wm', 'iconphoto', settingsDialogBox._w, img)
	
	mainSettingsFrame = guiUtils.createFrame(settingsDialogBox, tk.LEFT, fill="both", expand=True)

	#exampleCanvas = tk.Canvas(settingsDialogBox, bg="white")
	#exampleCanvas.pack(side=tk.RIGHT, fill="both", expand=True)

	# Simulation
	ttk.Label(mainSettingsFrame, text="Simulation", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)
	simulationSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.TOP, padding=(5, 5, 5, 5), ipady=10, anchor = tk.W)

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

	makeLastSimulationQuantineFrame = guiUtils.createFrame(simulationSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(makeLastSimulationQuantineFrame, text="Make last simulation quantine : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	makeLastSimulationQuantineCheckbox = ttk.Checkbutton(makeLastSimulationQuantineFrame, variable=tk.IntVar())
	makeLastSimulationQuantineCheckbox.pack(side=tk.RIGHT)
	makeLastSimulationQuantineCheckbox.state(["selected"])

	# Agents
	ttk.Label(mainSettingsFrame, text="Agents", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)
	agentSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.TOP, padding=(5, 5, 5, 5), ipady=10, anchor = tk.W)

	maximumSpeedFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(maximumSpeedFrame, text="Maximum agent speed (pixels/s) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	maximumSpeedEntry = ttk.Entry(maximumSpeedFrame, width=3)
	maximumSpeedEntry.pack(side=tk.RIGHT)
	maximumSpeedEntry.insert(0, "96")

	agentSizeFrame = guiUtils.createFrame(agentSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(agentSizeFrame, text="Agent size (pixels) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)	
	agentSizeEntry = ttk.Entry(agentSizeFrame, width=3)
	agentSizeEntry.pack(side=tk.RIGHT)
	agentSizeEntry.insert(0, "10")

	# Agents behavior
	ttk.Label(mainSettingsFrame, text="Behaviors", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)
	agentBehaviorSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.TOP, padding=(5, 5, 5, 5), ipady=10, anchor = tk.W)

	enableCentralTravelFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(enableCentralTravelFrame, text="Enable central travel : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	enableCentralTravelCheckbox = ttk.Checkbutton(enableCentralTravelFrame, variable=tk.IntVar())
	enableCentralTravelCheckbox.pack(side=tk.RIGHT)
	enableCentralTravelCheckbox.state(["selected"])  # Solution for ttk not having select() function.

	centralBehaviorChanceFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(centralBehaviorChanceFrame, text="Central travel chance (0-100) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	centralBehaviorChanceEntry = ttk.Entry(centralBehaviorChanceFrame, width=3)
	centralBehaviorChanceEntry.pack(side=tk.RIGHT)
	centralBehaviorChanceEntry.insert(0, "5")

	centerRangeFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(centerRangeFrame, text="Center range (pixels) : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	centerRangeEntry = ttk.Entry(centerRangeFrame, width=3)
	centerRangeEntry.pack(side=tk.RIGHT)
	centerRangeEntry.insert(0, "30")

	enableHumanLogicFrame = guiUtils.createFrame(agentBehaviorSettingsFrame, tk.TOP, anchor = tk.W)
	ttk.Label(enableHumanLogicFrame, text="Enable human logic : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
	enableHumanLogicCheckbox = ttk.Checkbutton(enableHumanLogicFrame, variable=tk.IntVar())
	enableHumanLogicCheckbox.pack(side=tk.RIGHT)
	enableHumanLogicCheckbox.state(["selected"])

	# Virus
	ttk.Label(mainSettingsFrame, text="Virus", padding=(5, 5, 5, 5), font=("Helvetica", 10, "bold")).pack(side=tk.TOP)
	virusSettingsFrame = guiUtils.createFrame(mainSettingsFrame, tk.TOP, padding=(5, 5, 5, 5), ipady=10, anchor = tk.W)

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
	ttk.Label(defaultRecoveryChanceFrame, text="Default recovery chance per second (0-100)/10 : ", padding=(5, 5, 5, 5)).pack(side=tk.LEFT)
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
		config["isLastSimulationQuarantine"] = makeLastSimulationQuantineCheckbox.state()[0] == "selected"
		config["maximumAgentSpeed"] = int(maximumSpeedEntry.get())
		config["agentSize"] = int(agentSizeEntry.get())
		config["enableCentralTravel"] = enableCentralTravelCheckbox.state()[0] == "selected"
		config["centralTravelChance"] = int(centralBehaviorChanceEntry.get())
		config["centerRange"] = int(centerRangeEntry.get())
		config["enableHumanLogic"] = enableHumanLogicCheckbox.state()[0] == "selected"
		config["infectiveRange"] = int(infectiveRangeEntry.get())
		config["infectionRisk"] = int(infectionChanceEntry.get())
		config["defaultRecoveryChance"] = int(defaultRecoveryChanceEntry.get())
		config["recoveryChanceProgress"] = int(recoveryChanceProgressEntry.get())
		config["deathRisk"] = int(deathRiskEntry.get())

		# We apply the limits
		config["simulationQuantity"] = min(max(config["simulationQuantity"], 1),15)
		config["canvasWidth"] = min(max(config["canvasWidth"], 1), 300)
		config["canvasHeight"] = min(max(config["canvasHeight"], 1), 300)
		config["centralTravelChance"] = min(max(config["centralTravelChance"], 0), 100)
		config["infectionRisk"] = min(max(config["infectionRisk"], 0), 100)
		config["defaultRecoveryChance"] = min(max(config["defaultRecoveryChance"], 0), 100)
		config["recoveryChanceProgress"] = min(max(config["recoveryChanceProgress"], 0), 100)
		config["deathRisk"] = min(max(config["deathRisk"], 0), 100)

		# We apply the necessary tweaks
		config["centralTravelChance"] = config["centralTravelChance"] / 100
		config["infectionRisk"] = config["infectionRisk"] / 100
		config["defaultRecoveryChance"] = config["defaultRecoveryChance"] / 100 / 10
		config["recoveryChanceProgress"] = config["recoveryChanceProgress"] / 100 / 1000
		config["deathRisk"] = config["deathRisk"] / 100 / 10

		# We adapt to the framerate where necessary
		config["maximumAgentSpeed"] /= config["framerate"]
		config["centralTravelChance"] /= config["framerate"]
		config["infectionRisk"] /= config["framerate"]
		config["defaultRecoveryChance"] /= config["framerate"]
		config["recoveryChanceProgress"] /= config["framerate"]
		config["deathRisk"] /= config["framerate"]
		
		return config
	
	# Bottom frame
	bottomFrame = guiUtils.createFrame(mainSettingsFrame, tk.BOTTOM, padding=(5, 5, 5, 5))
	ttk.Button(bottomFrame, text="Start", padding=(2, 2, 2, 2)).pack(side=tk.LEFT)
	ttk.Button(bottomFrame, text="Preview", command=lambda: spawnExampleCanvas(settingsDialogBox, generateConfigFromEntries()), padding=(2, 2, 2, 2)).pack(side=tk.RIGHT)

def spawnExampleCanvas(root, settings):
	pass
