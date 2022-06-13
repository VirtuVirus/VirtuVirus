# External Imports
from tkinter import *
from tkinter import ttk
from time import sleep
from random import randint, random
from sys import platform
from math import sqrt

# Internal Imports from modules folder
from modules_folder.simulation import *
from modules_folder.utilities import *
from modules_folder.config_vars import *
from modules_folder.global_vars import *

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
	createThread(AgentMovementThreads, moveAgent, (agent,))

	if type == "Infected":
		createThread(InfectionThreads, infectAgent, (agent,))
	elif type == "Immune":
		ImmunizeAgent(agent)
	else:
		SaneAgents.append(agent)
	return agent

def ImmunizeAgent(agent):
	if agent in DeadAgents:
		return
	if agent not in ImmuneAgents:
		ImmuneAgents.append(agent)
	else:
		return

	canvas.itemconfig(agent, fill="green")

	if agent in InfectedAgents:
		InfectedAgents.remove(agent)
	return

def KillAgent(agent):
	if agent not in DeadAgents:
		DeadAgents.append(agent)
	else:
		return

	canvas.itemconfig(agent, fill="grey")
	canvas.tag_lower(agent)

	if agent in SaneAgents: #In case of bug
		SaneAgents.remove(agent)
	if agent in InfectedAgents:
		InfectedAgents.remove(agent)
	return

def infectAgent(agent):
	if agent in DeadAgents or agent in InfectedAgents:
		return

	canvas.itemconfig(agent, fill="red")

	# We create the infectious zone and append it.
	agent_infectious_zone = canvas.create_oval(0, 0, 0+(size*infective_range), 0+(size*infective_range), )
	InfectedZones.append(agent_infectious_zone)

	# We set the default Recovery chance progression
	localRecoveryChanceProgress = 0

	# We add the agent to the infected agents.
	if agent in SaneAgents:
		SaneAgents.remove(agent)
	if agent not in InfectedAgents:
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
			if overlapping_agent != agent and overlapping_agent != agent_infectious_zone and overlapping_agent in SaneAgents:
				if random() < infectionChance: # Give them a chance to escape unharmed.
					createThread(InfectionThreads, infectAgent, (overlapping_agent,))
		
		# Very low chance for the agent to be immunized.
		if random() < defaultRecoveryChance + localRecoveryChanceProgress or cureSignal == True:
			ImmunizeAgent(agent)
			canvas.delete(agent_infectious_zone)
			return
		localRecoveryChanceProgress += defaultRecoveryChanceProgress

		# Low chance for the agent to die. If Human Behaviors are enabled, the chance gets higher with the number of infected people.
		if (random() < deathRisk - localRecoveryChanceProgress/4) or (random() < deathRisk * len(InfectedAgents)/(len(SaneAgents)+len(ImmuneAgents)) - localRecoveryChanceProgress/4 and doHumanBehaviors == True):
			KillAgent(agent)
			canvas.delete(agent_infectious_zone)
			return

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
		if agent not in Agents or len(AgentMovementThreads) == 0 or agent in DeadAgents:
			return

		# Central Behavior
		if centralBehavior == True:
			centralBehaviorChance = random()

			if doHumanBehaviors:
				# If the agent is infected, we make the chance lower.
				if agent in InfectedAgents:
					centralBehaviorChance *= 3
				# If there are lots of infected, we make the chance lower.
				if agent in SaneAgents:
					centralBehaviorChance /= (len(Agents) - len(InfectedAgents)+len(DeadAgents)*3)/len(Agents)
			
			if centralBehaviorChance <= centralBehaviorChanceRequirement:
				(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
				(CenterX, CenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)

				testCordX, testCordY = getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

				while SimulationStopSignal == False and centralBehavior == True and sqrt(testCordX**2 + testCordY**2) > centralBehaviorRange :
					# Go to center
					local_x_speed, local_y_speed = (WIDTH/2 - CenterX)/framerate, (HEIGHT/2 - CenterY)/framerate
					canvas.move(agent, local_x_speed, local_y_speed)

					try:
						(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos) = canvas.coords(agent)
					except:
						return
					(CenterX, CenterY) = get2CenterCoordsFrom4Coords(AgentLeftPos, AgentTopPos, AgentRightPos, AgentBottomPos)
					testCordX, testCordY = getCentralCenterCordsFromTopLeftCords(CenterX, CenterY)

					if SimulationStopSignal or len(AgentMovementThreads) == 0 or agent in DeadAgents:
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
	style.theme_use('vista')
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
