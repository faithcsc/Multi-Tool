import json
import time
from classes.functions import Functions

class Snowager:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Snowager(self, username):
        self.functions.createTaskData('Snowager', username)
        if time.time() - float(self.functions.lastRun('Snowager', username)) >= 10800:
            resp = self.neo.get('winter/snowager2.phtml', 'http://www.neopets.com/winter/snowager.phtml')
            if not self.functions.contains(resp.text, 'You dont want to try and enter again'):
                if self.functions.contains(resp.text, 'icy blast at you'):
                    if self.functions.contains(resp.text, 'You are now eligible to use'):
                        self.functions.log('Snowager: Blasted - Received Avatar')
                    else:
                        self.functions.log('Snowager: Blasted')
                else:
                    self.functions.log('Snowager: Done')
            else:
                self.functions.log('Snowager: It\'s too soon to visit')
            self.functions.updateLastRun('Snowager', username)