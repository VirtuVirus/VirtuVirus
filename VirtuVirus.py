# Internal Modules
from modules import guiBase
from modules import sharedData

GraphicalComponents = guiBase.defineGUI()
sharedData.writeGlobalVar("interactiveGraphicalComponents",GraphicalComponents)

GraphicalComponents["mainWindowRoot"].mainloop()
