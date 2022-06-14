# ---------------------------------------------------------- Config ----------------------------------------------------------
# Window size
WIDTH, HEIGHT = 800, 600						# Size of the window.

# Simulation config
framerate = 24									# Define framerate here. It's the basis for the interval between each frame of the simulation.
canvasQuantity = 4							# Number of canvases in the simulation.

# Agents
maxXSpeed = maxYSpeed = 96						# Speed of the agents.
size = 10										# Size of the agents.
centralBehaviorChanceRequirement = 0.05						# Chance of the central behavior to be activated per second.
centralBehaviorRange = 30						# Range of the central area the agents will try to get to.
doHumanBehaviors = True							# Agents' actions will depend on the number of infected.

# Virus
infective_range = 4								# Range of infection is defined by the size multiplied by this number.
infectionChance = 0.48							# Chance per second for the agent to be infected.
defaultRecoveryChance = 0.024					# Chance to recover by default on each second.
defaultRecoveryChanceProgress = 0.00036			# Progression on each second
deathRisk = 0.018								# Death risk per second.

# Keep config stable no matter the framerate
frequency = 1/framerate							# Controls the interval the agents wait before performing their routines (movement, infection, etc...) again. Preferred value is 0.04.
maxXSpeed = maxYSpeed = maxYSpeed/framerate		# Movement gained per frame.
centralBehaviorChanceRequirement /= framerate
infectionChance /= framerate					# Chance per FRAME for the agent to be infected.
defaultRecoveryChance /= framerate				# Chance to recover by default on each frame.
defaultRecoveryChanceProgress /= framerate		# Progression on each frame
deathRisk /= framerate							# Death risk per frame.