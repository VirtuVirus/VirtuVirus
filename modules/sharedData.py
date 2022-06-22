# This module tremendously helps by reuniting everything that is shared between the modules in only one place.
# No constant imports necessary like the older version.
# The variables are only accessible using these functions to keep everything synchronized.

# To be honest, I'm not certain this is necessary, but it WILL avoid me issues I've had in the past.

from modules import defaultConfigVars

# ----------------------------------------- Config ----------------------------------------- #
config = defaultConfigVars.config

def setConfig(incomingConfig):
	global config
	config = incomingConfig

def getCurrentConfig():
	global config
	return config

def getVarInConfig(varName):
	global config
	return config[varName]

# ----------------------------------------- Global Variables ----------------------------------------- #
globalVars = {}

def getGlobalVar(varName):
	global globalVars
	return globalVars[varName]

def writeGlobalVar(varName, varValue):
	global globalVars
	globalVars[varName] = varValue

def getAllGlobalVars():
	global globalVars
	return globalVars
