# Imports
from tkinter import *
from time import sleep
from threading import Thread
from random import randint, random

# Config
WIDTH, HEIGHT = 800, 600		# Size of the window.
maxYSpeed = maxYSpeed = 4		# Speed of the agents.
size = 10						# Size of the agents.
infective_range = 4				# Range of infection is defined by the size multiplied by this number.
frequency = 0.04				# Controls the interval the agents wait before performing their routines (movement, infection, etc...) again.
infectionChance = 0.1
numberOfAgents = 49
numberOfInfectedAgents = 1

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
		sleep(0.001) # This trick prevents the agents from all running their checks at the EXACT same time. Helps against lag.

def createAgent(isInfected):
	global size
	
	x_position, y_position = randint(0, WIDTH), randint(0, HEIGHT)

	agent = canvas.create_oval(x_position, y_position, x_position+size, y_position+size, fill="blue")

	thread_movement = createThread(AgentMovementThreads, moveAgent, (agent,))

	if isInfected:
		thread_infectious = createThread(InfectionThreads, infectAgent, (agent,))

	return agent

def infectAgent(agent):
	canvas.itemconfig(agent, fill="red")

	global infective_range

	agent_infectious_zone = canvas.create_oval(0, 0, 0+(size*infective_range), 0+(size*infective_range), )

	while shutdown == False:
		# Get cords
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
			if overlapping_agent != agent and overlapping_agent != agent_infectious_zone:
				if canvas.itemcget(overlapping_agent, "fill") == "blue" and random() >= (1 - infectionChance): # Only infect uninfected agents, and give them a chance to escape unharmed.
					canvas.itemconfig(overlapping_agent, fill="red")
					createThread(InfectionThreads, infectAgent, (overlapping_agent,))

		sleep(frequency * 0.8)

def moveAgent(agent):
	global maxYSpeed, maxYSpeed, shutdown

	local_x_speed, local_y_speed = maxYSpeed*random(), maxYSpeed*random()

	if randint(0, 1) == 1:
		local_x_speed *= -1
	if randint(0, 1) == 1:
		local_y_speed *= -1

	while shutdown == False:
		canvas.move(agent, local_x_speed, local_y_speed)

		(leftPos, topPos, rightPos, bottomPos) = canvas.coords(agent)

		if leftPos <= 0 or rightPos >= WIDTH:
			local_x_speed = -local_x_speed
		if topPos <= 0 or bottomPos >= HEIGHT:
			local_y_speed = -local_y_speed
		sleep(frequency)

# Program
root = Tk()
root.title("VirtuVirus")

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

shutdown = False

AgentMovementThreads = []
InfectionThreads = []
DefaultThreads = []

def main():
	createAgents(numberOfAgents, False)
	createAgents(numberOfInfectedAgents, True)
MainThread = createThread(DefaultThreads, main, ())

root.mainloop()