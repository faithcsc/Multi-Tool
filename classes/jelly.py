import time
import random
from classes.functions import Functions

class Jelly:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Jelly(self, username):
        self.functions.createTaskData('Jelly', username)
        if time.time() - float(self.functions.lastRun('Jelly', username)) >= 86400:
            resp = self.neo.post('jelly/jelly.phtml', {'type': 'get_jelly'}, 'http://www.neopets.com/jelly/jelly.phtml')
            if self.functions.contains(resp.text, 'You take some <b>'):
                result = self.functions.getBetween(resp.text, 'some <b>', '</b>!!!')
                self.functions.log('Giant Jelly: Grabbed %s' % result)
            self.functions.updateLastRun('Jelly', username)