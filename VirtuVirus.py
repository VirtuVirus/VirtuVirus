# External Modules
import tkinter as tk
from time import sleep

# Internal Modules
from modules import guiBase
from modules import utilities
from modules import sharedData

GraphicalComponents = guiBase.defineGUI()

sharedData.writeGlobalVar("interactiveGraphicalComponents",GraphicalComponents)

GraphicalComponents["mainWindowRoot"].mainloop()
