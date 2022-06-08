# Imports
from tkinter import *
from time import sleep
from threading import Thread
from random import randint, random
from sys import platform

# Config
WIDTH, HEIGHT = 800, 600		# Size of the window.
maxYSpeed = maxYSpeed = 4		# Speed of the agents.
size = 10						# Size of the agents.
infective_range = 4				# Range of infection is defined by the size multiplied by this number.
frequency = 0.04				# Controls the interval the agents wait before performing their routines (movement, infection, etc...) again.
infectionChance = 0.02			# Chance per FRAME for the agent to be infected.

# ---------------------------------------------------------- Utilities ----------------------------------------------------------
def createThread(array, target, args):
	thread = Thread(target=target, args=args)
	thread.daemon = True
	thread.start()
	array.append(thread)
	return thread

def get2CenterCoordsFrom4Coords(leftPos, topPos, rightPos, bottomPos):
	return ((leftPos+rightPos)/2, (topPos+bottomPos)/2)

# -------------------------------------------------------- Agents Functions ------------------------------------------------------
def createAgents(quantity, areInfected):
	for i in range(quantity):
		createAgent(areInfected)
		sleep(0.005) # This trick prevents the agents from all running their checks at the EXACT same time. Helps against lag.

def createAgent(isInfected):
	global size
	
	# Randomly place the agent.
	x_position, y_position = randint(0, WIDTH), randint(0, HEIGHT)

	agent = canvas.create_oval(x_position, y_position, x_position+size, y_position+size, fill="blue")
	Agents.append(agent)

	# We give it movement
	thread_movement = createThread(AgentMovementThreads, moveAgent, (agent,))
	AgentMovementThreads.append(thread_movement)

	if isInfected:
		thread_infectious = createThread(InfectionThreads, infectAgent, (agent,))
		InfectionThreads.append(thread_infectious)
	else:
		SaneAgents.append(agent)

	return agent

def infectAgent(agent):
	canvas.itemconfig(agent, fill="red")

	global infective_range, SimulationStopControl, infectionChance

	# We create the infectious zone and append it.
	agent_infectious_zone = canvas.create_oval(0, 0, 0+(size*infective_range), 0+(size*infective_range), )
	InfectedZones.append(agent_infectious_zone)

	# We add the agent to the infected agents.
	if(agent in SaneAgents):
		SaneAgents.remove(agent)
	if(agent not in InfectedAgents):
		InfectedAgents.append(agent)

	while SimulationStopControl == False:
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
			if overlapping_agent != agent and overlapping_agent != agent_infectious_zone and overlapping_agent in SaneAgents:
				if random() > (1 - infectionChance): # Give them a chance to escape unharmed.
					canvas.itemconfig(overlapping_agent, fill="red")
					createThread(InfectionThreads, infectAgent, (overlapping_agent,))

		sleep(frequency * 0.8)
	return

def moveAgent(agent):
	global maxYSpeed, maxYSpeed, SimulationStopControl

	# Generate random starter movement
	local_x_speed, local_y_speed = maxYSpeed*random(), maxYSpeed*random()
	if randint(0, 1) == 1:
		local_x_speed *= -1
	if randint(0, 1) == 1:
		local_y_speed *= -1

	while SimulationStopControl == False:
		# Make the agents bounce against the screen borders.
		canvas.move(agent, local_x_speed, local_y_speed)

		(leftPos, topPos, rightPos, bottomPos) = canvas.coords(agent)

		if leftPos <= 0 or rightPos >= WIDTH:
			local_x_speed = -local_x_speed
		if topPos <= 0 or bottomPos >= HEIGHT:
			local_y_speed = -local_y_speed
		sleep(frequency)
	return

def stopSimulation():
	global SimulationStopControl
	# Indicate that the simulation is stopping.
	SimulationStopControl = True

	# Wait for all threads to stop.
	if(len(Agents) < 40):
		for thread in AgentMovementThreads:
			thread.join()
		for thread in InfectionThreads:
			thread.join()
		
		InfectionThreads.clear()
		AgentMovementThreads.clear()
		InfectedZones.clear()
	else: # Waiting the normal way becomes unstable after approximately 30 agents, and can freeze. Better cause errors than a complete crash.
		InfectionThreads.clear()
		AgentMovementThreads.clear()
		InfectedZones.clear()

		sleep(1)

	SimulationStopControl = False

	return

def clearSimulation():
	stopSimulation()

	# Clear the canvas.
	canvas.delete("all")

	# Clear the lists.
	Agents.clear()
	SaneAgents.clear()
	InfectedAgents.clear()

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

# Create frame at the top
frame = Frame(root)
frame.pack(side=TOP)

# Create canvas
canvas = Canvas(frame, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack(side=RIGHT)

# Add controls to the left of the frame
controls = Frame(frame)
controls.pack(side=LEFT, padx=10)

# Add controls label
controls_label = Label(controls, text="Controls")
controls_label.pack(pady=10)

# Add button to the left that adds agents
add_agents_button = Button(controls, text="Add agents", command=lambda: createAgents(10, False))
add_agents_button.pack(side=TOP)
# Add button to the left that adds infected agents
add_infected_agents_button = Button(controls, text="Add infected agent", command=lambda: createAgent(True))
add_infected_agents_button.pack(side=TOP)
# Add button to stop simulation
stop_button = Button(controls, text="Stop", command=lambda: stopSimulation())
stop_button.pack(side=TOP)
# Add button to clear the canvas
clear_button = Button(controls, text="Clear", command=lambda: clearSimulation())
clear_button.pack(side=TOP)

# Variable
SimulationStopControl = False

# We configure the lists.
Agents = []
SaneAgents = []
InfectedAgents = []
InfectedZones = []

AgentMovementThreads = []
InfectionThreads = []
DefaultThreads = []

# Main thread, since root.mainloop() blocks the program.
def main():
	# Add statistics to the right of the window.
	statistics = Label(root, text="Statistics : Agents = "+str(len(Agents))+" | Sane = "+str(len(SaneAgents))+" | Infected = "+str(len(InfectedAgents)))
	statistics.pack(side=LEFT)

	# Update statistics
	while True:
		sleep(1)
		statistics.config(text="Statistics : Agents = "+str(len(Agents))+" | Sane = "+str(len(SaneAgents))+" | Infected = "+str(len(InfectedAgents)))
MainThread = createThread(DefaultThreads, main, ())

root.mainloop()