# ---------------------------------------------------------- Config ----------------------------------------------------------
# Window size
WIDTH, HEIGHT = 800, 600						# Size of the window.

config = {}

# Simulation config
config["simulationQuantity"] = 4
config["framerate"] = 24									# Define framerate here. It's the basis for the interval between each frame of the simulation.
config["canvasWidth"] = 300
config["canvasHeight"] = 300							# Number of canvases in the simulation.
config["isLastSimulationQuarantine"] = True

# Agents
config["numberOfSaneAgents"] = 99							# Number of sane agents in a simulation.
config["numberOfInfectedAgents"] = 1						# Number of infected agents in a simulation.
config["numberOfImmuneAgents"] = 0						# Number of immune agents in a simulation.
config["maximumAgentSpeed"] =  96						# Speed of the agents.
config["agentSize"] = 10										# Size of the agents.
config["enableCentralTravel"] = True
config["centralTravelChance"] = 0.05						# Chance of the central behavior to be activated per second.
config["centerRange"] = 30						# Range of the central area the agents will try to get to.
config["enableHumanLogic"] = True							# Agents' actions will depend on the number of infected.

# Virus
config["infectiveRange"] = 4								# Range of infection is defined by the size multiplied by this number.
config["infectionRisk"] = 0.48							# Chance per second for the agent to be infected.
config["defaultRecoveryChance"] = 0.024					# Chance to recover by default on each second.
config["recoveryChanceProgress"] = 0.00036			# Progression on each second
config["deathRisk"] = 0.018								# Death risk per second.

# Keep config stable no matter the framerate
config["maximumAgentSpeed"] /= config["framerate"]		# Movement gained per frame.
config["centralTravelChance"] /= config["framerate"]
config["infectionRisk"] /= config["framerate"]					# Chance per FRAME for the agent to be infected.
config["defaultRecoveryChance"] /= config["framerate"]				# Chance to recover by default on each frame.
config["recoveryChanceProgress"] /= config["framerate"]		# Progression on each frame
config["deathRisk"] /= config["framerate"]							# Death risk per frame.
