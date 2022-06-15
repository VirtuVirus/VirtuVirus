# External Imports
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
from sys import platform
from PIL import Image, ImageTk

# Internal Imports
from modules import configVars
from modules import guiUtils

def defineGUI():
	global logo

	root = tk.Tk()
	root.title("VirtuVirus")
	root.iconname("VirtuVirus")
	root.minsize(configVars.WIDTH, configVars.HEIGHT)
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
	logoFile = logoFile.resize((int(configVars.WIDTH/5.2), int(configVars.HEIGHT/4)), Image.ANTIALIAS)
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
	settingsDialogBox.minsize(700, 500)
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