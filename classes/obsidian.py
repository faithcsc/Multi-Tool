import time
import random
from classes.functions import Functions

class Obsidian:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Obsidian(self, username):
        self.functions.createTaskData('Obsidian', username)
        if time.time() - float(self.functions.lastRun('Obsidian', username)) >= 86400:
            resp = self.neo.get('magma/quarry.phtml', 'https://thedailyneopets.com/dailies')
            if self.functions.contains(resp.text, 'Shiny Obsidian'):
                self.functions.log('Obsidian Quarry: Received Shiny Obsidian')
            self.functions.updateLastRun('Obsidian', username)