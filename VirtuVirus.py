# External Modules
import tkinter as tk
from time import sleep

# Internal Modules
from modules import guiBase
from modules import guiUtils
from modules import utilities

GraphicalComponents = guiBase.defineGUI()

TestThreads = []
def testProcedure(Type):
	sleep(2)
	print("Testing procedure process started for " + Type)
	if Type == "canvasses":
		guiUtils.generateCanvass(GraphicalComponents["simulation_zone"], 15, 300, 300, GraphicalComponents["window_root"], True)
	else:
		print("Unknown test. Ignoring...")
#utilities.createThread(TestThreads, testProcedure, ("canvasses",))

GraphicalComponents["window_root"].mainloop()
