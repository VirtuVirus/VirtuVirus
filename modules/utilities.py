# External Imports
from threading import Thread

# Internal Imports
from modules import defaultConfigVars

def createThread(ThreadManagementArray, function, arguments=()):
	thread = Thread(target=function, args=arguments)
	thread.daemon = True
	thread.start()
	ThreadManagementArray.append(thread)
	return thread

def get2CenterCoordsFrom4Coords(leftPos, topPos, rightPos, bottomPos):
	return ((leftPos+rightPos)/2, (topPos+bottomPos)/2)

def getCentralCenterCordsFromTopLeftCords(CenterX, CenterY):
	return (CenterX - defaultConfigVars.WIDTH/2, CenterY - defaultConfigVars.HEIGHT/2)
