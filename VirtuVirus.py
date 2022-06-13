# External Imports
from tkinter import *
from tkinter import ttk
from time import sleep

# Internal Imports from modules folder
from modules_folder.simulation import clearSimulation, stopSimulation, ToggleCentralBehavior
from modules_folder.agents import createAgents, createAgent
from modules_folder.utilities import createThread
from modules_folder.gui_base import *
from modules_folder.config_vars import *
from modules_folder.global_vars import *

# Add button to the left that adds agents
add_agents_button = ttk.Button(controls, text="Add agents", command=lambda: createAgents(10, "Sane"))
add_agents_button.pack(side=TOP)
# Add button to the left that adds infected agents
add_infected_agents_button = ttk.Button(controls, text="Add infected agent", command=lambda: createAgent("Infected"))
add_infected_agents_button.pack(side=TOP)
# Add button to toggle Central Behavior
central_behavior_button = ttk.Button(controls, text="Toggle Central Behavior", command=ToggleCentralBehavior)
central_behavior_button.pack(side=TOP)
# Add button to stop simulation
stop_button = ttk.Button(controls, text="Stop", command=lambda: stopSimulation())
stop_button.pack(side=TOP)
# Add button to clear the canvas
clear_button = ttk.Button(controls, text="Clear", command=lambda: clearSimulation())
clear_button.pack(side=TOP)

# Main thread, since root.mainloop() blocks the program.
def main():
	# Add statistics to the right of the window.
	statistics = ttk.Label(root, text="Statistics : Agents = "+str(len(Agents))+" | Sane = "+str(len(SaneAgents))+" | Infected = "+str(len(InfectedAgents))+" | Immune = "+str(len(ImmuneAgents))+" | Dead = "+str(len(DeadAgents)))
	statistics.pack(side=LEFT)

	# Update statistics
	while True:
		sleep(1)
		statistics.config(text="Statistics : Agents = "+str(len(Agents))+" | Sane = "+str(len(SaneAgents))+" | Infected = "+str(len(InfectedAgents))+" | Immune = "+str(len(ImmuneAgents))+" | Dead = "+str(len(DeadAgents)))
MainThread = createThread(DefaultThreads, main, ())

root.mainloop()
