# Imports
from tkinter import *
from tkinter import ttk
from time import sleep
from threading import Thread
from random import randint, random
from sys import platform
from math import sqrt

# ---------------------------------------------------------- Config ----------------------------------------------------------
# Simulation config
WIDTH, HEIGHT = 800, 600						# Size of the window.
framerate = 24									# Define framerate here. It's the basis for the interval between each frame of the simulation.

# Agents
maxXSpeed = maxYSpeed = 96						# Speed of the agents.
size = 10										# Size of the agents.
centralBehaviorChance = 0.1						# Chance of the central behavior to be activated per second.
centralBehaviorRange = 30						# Range of the central area the agents will try to get to.
doHumanThinking = True							# Agents' actions will depend on the number of infected.

# Virus
infective_range = 4								# Range of infection is defined by the size multiplied by this number.
infectionChance = 0.48							# Chance per second for the agent to be infected.
defaultRecoveryChance = 0.024					# Chance to recover by default on each second.
defaultRecoveryChanceProgress = 0.00036			# Progression on each second

# Keep config stable no matter the framerate
frequency = 1/framerate							# Controls the interval the agents wait before performing their routines (movement, infection, etc...) again. Preferred value is 0.04.
maxXSpeed = maxYSpeed = maxYSpeed/framerate		# Movement gained per frame.
centralBehaviorChance /= framerate
infectionChance /= framerate					# Chance per FRAME for the agent to be infected.
defaultRecoveryChance /= framerate				# Chance to recover by default on each frame.
defaultRecoveryChanceProgress /= framerate		# Progression on each frame


# ---------------------------------------------------------- Utilities ----------------------------------------------------------
def createThread(array, target, args):
	thread = Thread(target=target, args=args)
	thread.daemon = True
	thread.start()
	array.append(thread)
	return thread

def get2CenterCoordsFrom4Coords(leftPos, topPos, rightPos, bottomPos):
	return ((leftPos+rightPos)/2, (topPos+bottomPos)/2)

def getCentralCenterCordsFromTopLeftCords(CenterX, CenterY):
	return (CenterX - WIDTH/2, CenterY - HEIGHT/2)

# -------------------------------------------------------- Agents Functions ------------------------------------------------------
def createAgents(quantity, type):
	for i in range(quantity):
		createAgent(type)
		sleep(0.005) # This trick prevents the agents from all running their checks at the EXACT same time. Helps against lag.
	return

def createAgent(type):
	global size
	
	# Randomly place the agent.
	x_position, y_position = randint(0, WIDTH), randint(0, HEIGHT)

	agent = canvas.create_oval(x_position, y_position, x_position+size, y_position+size, fill="blue")
	Agents.append(agent)

	# We give it movement
	thread_movement = createThread(AgentMovementThreads, moveAgent, (agent,))
	AgentMovementThreads.append(thread_movement)

	if type == "Infected":
		thread_infectious = createThread(InfectionThreads, infectAgent, (agent,))
		InfectionThreads.append(thread_infectious)
	elif type == "Immune":
		ImmunizeAgent(agent)
	else:
		SaneAgents.append(agent)
	return agent

def ImmunizeAgent(agent):
	canvas.itemconfig(agent, fill="green")

	ImmuneAgents.append(agent)
	if agent in InfectedAgents:
		InfectedAgents.remove(agent)
	return

def infectAgent(agent):
	canvas.itemconfig(agent, fill="red")

	# We create the infectious zone and append it.
	agent_infectious_zone = canvas.create_oval(0, 0, 0+(size*infective_range), 0+(size*infective_range), )
	InfectedZones.append(agent_infectious_zone)

	# We set the default Recovery chance progression
	localRecoveryChanceProgress = 0

	# We add the agent to the infected agents.
	if(agent in SaneAgents):
		SaneAgents.remove(agent)
	if(agent not in InfectedAgents):
		InfectedAgents.append(agent)

	while SimulationStopSignal == False:
		# Get cords of the agents and the agents' infectious zone.
		(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
		(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos) = canvas.coords(agent_infectious_zone)

		# Get center cords
		(AgentCenterX, AgentCenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
		(InfectCenterX, InfectCenterY) = get2CenterCoordsFrom4Coords(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos)

		# Move agent_infectious_zone to the agent's position
		canvas.move(agent_infectious_zone, AgentCenterX-InfectCenterX, AgentCenterY-InfectCenterY)

		# Infect overlapping agents
		overlapping_agents = canvas.find_overlapping(InfectLeftPos, InfectTopPos, InfectRightPos, InfectBottomPos)
		for overlapping_agent in overlapping_agents:
			if overlapping_agent != agent and overlapping_agent != agent_infectious_zone and overlapping_agent in SaneAgents and overlapping_agent not in ImmuneAgents:
				if random() < infectionChance: # Give them a chance to escape unharmed.
					canvas.itemconfig(overlapping_agent, fill="red")
					createThread(InfectionThreads, infectAgent, (overlapping_agent,))
		
		# Very low chance for the agent to be immunized.
		if random() < defaultRecoveryChance + localRecoveryChanceProgress or cureSignal == True:
			ImmunizeAgent(agent)
			canvas.delete(agent_infectious_zone)
			return
		localRecoveryChanceProgress += defaultRecoveryChanceProgress

		if SimulationStopSignal:
			return
		sleep(frequency * 0.8)
	return

def moveAgent(agent):
	# Generate random starter movement
	local_x_speed, local_y_speed = maxXSpeed*random(), maxYSpeed*random()
	if randint(0, 1) == 1:
		local_x_speed *= -1
	if randint(0, 1) == 1:
		local_y_speed *= -1

	while SimulationStopSignal == False:
		# Prevent thread surviving
		if agent not in Agents or len(AgentMovementThreads) == 0:
			return

		# Central Behavior
		if centralBehavior == True:
			chanceToLaunchCentralBehavior = random()

			if doHumanThinking:
				# If the agent is infected, we make the chance lower.
				if agent in InfectedAgents:
					chanceToLaunchCentralBehavior /= 3
				# If there are lots of infected, we make the chance lower.
				if agent in SaneAgents:
					chanceToLaunchCentralBehavior *= 1 - len(InfectedAgents)/len(Agents)
			
			if chanceToLaunchCentralBehavior >= (1 - centralBehaviorChance):
				(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
				(CenterX, CenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)

				testCordX, testCordY = getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

				while SimulationStopSignal == False and centralBehavior == True and sqrt(testCordX**2 + testCordY**2) > centralBehaviorRange :
					# Go to center
					local_x_speed, local_y_speed = (WIDTH/2 - CenterX)/framerate, (HEIGHT/2 - CenterY)/framerate
					canvas.move(agent, local_x_speed, local_y_speed)

					(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
					(CenterX, CenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
					testCordX, testCordY = getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

					if SimulationStopSignal:
						return
					sleep(frequency)
				
				# Regenerate starter movement
				local_x_speed, local_y_speed = maxXSpeed*random(), maxYSpeed*random()
				if randint(0, 1) == 1:
					local_x_speed *= -1
				if randint(0, 1) == 1:
					local_y_speed *= -1
		# Make the agents bounce against the screen borders.
		canvas.move(agent, local_x_speed, local_y_speed)
		try:
			(leftPos, topPos, rightPos, bottomPos) = canvas.coords(agent)
		except:
			return

		if leftPos <= 0 or rightPos >= WIDTH:
			local_x_speed = -local_x_speed
		if topPos <= 0 or bottomPos >= HEIGHT:
			local_y_speed = -local_y_speed
		
		if SimulationStopSignal:
			return
		sleep(frequency)
	return

def stopSimulation():
	global SimulationStopSignal
	# Indicate that the simulation is stopping.
	SimulationStopSignal = True

	# Wait
	sleep(frequency*5)

	# Clear the threads
	AgentMovementThreads.clear()
	InfectionThreads.clear()
	
	SimulationStopSignal = False
	return

def clearSimulation():
	stopSimulation()

	# Delete all the agents from the canvas
	for agent in Agents:
		canvas.delete(agent)
	for agent_infectious_zone in InfectedZones:
		canvas.delete(agent_infectious_zone)

	# Clear the lists.
	Agents.clear()
	SaneAgents.clear()
	InfectedAgents.clear()
	ImmuneAgents.clear()
	InfectedZones.clear()
	return

def ToggleCentralBehavior():
	global centralBehavior
	centralBehavior = not centralBehavior
	return

# ---------------------------------------------------------- Program ----------------------------------------------------------
root = Tk()
root.title("VirtuVirus")
root.iconname("VirtuVirus")
root.resizable(False, False)

# Set icon
if "win" in platform:
	root.wm_iconbitmap(default="assets/icon.ico")
else:
	img = PhotoImage(file='assets/icon.png')
	root.tk.call('wm', 'iconphoto', root._w, img)

# and theme
style = ttk.Style(root)
if "win" in platform:
	style.theme_use('winnative')
else:
	style.theme_use('clam')

# Create frame at the top
frame = ttk.Frame(root)
frame.pack(side=TOP)

# Create canvas
canvas = Canvas(frame, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack(side=RIGHT)

# Add controls to the left of the frame
controls = ttk.Frame(frame)
controls.pack(side=LEFT, padx=10)

# Add controls label
controls_label = ttk.Label(controls, text="Controls")
controls_label.pack(pady=10)

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

# Variable
centralBehavior = True
SimulationStopSignal = False
cureSignal = False

# We configure the lists.
Agents = []
SaneAgents = []
ImmuneAgents = []
InfectedAgents = []
InfectedZones = []

AgentMovementThreads = []
InfectionThreads = []
DefaultThreads = []

# Main thread, since root.mainloop() blocks the program.
def main():
	# Add statistics to the right of the window.
	statistics = ttk.Label(root, text="Statistics : Agents = "+str(len(Agents))+" | Sane = "+str(len(SaneAgents))+" | Infected = "+str(len(InfectedAgents))+" | Immune = "+str(len(ImmuneAgents)))
	statistics.pack(side=LEFT)

	# Update statistics
	while True:
		sleep(1)
		statistics.config(text="Statistics : Agents = "+str(len(Agents))+" | Sane = "+str(len(SaneAgents))+" | Infected = "+str(len(InfectedAgents))+" | Immune = "+str(len(ImmuneAgents)))
MainThread = createThread(DefaultThreads, main, ())

root.mainloop()
