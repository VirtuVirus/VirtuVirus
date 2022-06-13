# External Imports
from threading import Thread

# Internal Imports
from modules_folder.config_vars import *

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