import time
import random
from classes.functions import Functions

class FruitMachine:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def FruitMachine(self, username):
        self.functions.createTaskData('FruitMachine', username)
        if time.time() - float(self.functions.lastRun('FruitMachine', username)) >= 86400:
            resp = self.neo.get('desert/fruit/index.phtml', 'https://thedailyneopets.com/dailies')
            if not self.functions.contains(resp.text, 'Please come back tomorrow and try again'):
                result = self.functions.getBetween(resp.text, 'name="ck" value="', '">')
                resp = self.neo.post('desert/fruit/index.phtml', {'spin': '1', 'ck': result}, 'http://www.neopets.com/desert/fruit/index.phtml')
                if self.functions.contains(resp.text, 'Sorry, this is not a winning spin'):
                    self.functions.log('Fruit Machine: Done')
                else:
                    self.functions.log('Fruit Machine: You won!')
            self.functions.updateLastRun('FruitMachine', username)