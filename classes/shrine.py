import time
import random
from classes.functions import Functions

class Shrine:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Shrine(self, username):
        self.functions.createTaskData('Shrine', username)
        if time.time() - float(self.functions.lastRun('Shrine', username)) >= 46800:
            resp = self.neo.post('desert/shrine.phtml', {'type': 'approach'}, 'http://www.neopets.com/desert/shrine.phtml')
            if not self.functions.contains(resp.text, 'Maybe you should wait'):
                self.functions.log('Coltzans Shrine: Done')
            self.functions.updateLastRun('Shrine', username)