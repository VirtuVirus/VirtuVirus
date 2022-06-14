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
	placeholderCanvas = tk.Canvas(canvasZone, bg="grey")
	placeholderCanvas.pack(fill="both", expand=True)

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
	StartSimulationButton = guiUtils.createButton(StartAndStopZone, tk.LEFT, "Start", "pass", None, padding=(2, 2, 2, 2))
	StopSimulationButton = guiUtils.createButton(StartAndStopZone, tk.RIGHT, "Stop", "pass", None, padding=(2, 2, 2, 2))

	PauseSimulationButton = guiUtils.createButton(simulationControlZone, tk.TOP, "Pause Simulation", "pass", None)

	OpenSettingsButton = guiUtils.createButton(simulationControlZone, tk.TOP, "Modify Settings", "pass", None)
	ShowCurrentGraph = guiUtils.createButton(simulationControlZone, tk.TOP, "Show Graph", "pass", None)

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

	return {"window_root": root}