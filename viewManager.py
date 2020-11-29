
import sys

#-------------------------------------------------------------------------------
#
# Globals
#
#-------------------------------------------------------------------------------

g_viewManager = ViewManager()

class View:
    def __init__(self, name):
        g_viewManager.addView(self, name)

    def load(self):
        pass

    def unload(self):
        pass

class ViewManager:
    def __init__(self):
        self.viewDict = {}
        self.currView = None

    def addView(self, name, view):
        self.viewDict.add(name, view)

    def switchView(self, name):
        if self.viewDict.get(name):
            if self.currView is not None:
                self.currView.unload()
                self.currView = None
            self.viewDict[name].load()
            self.currView = this.viewDict[name]



