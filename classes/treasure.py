import time
import random
from classes.functions import Functions

class BuriedTreasure:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def BuriedTreasure(self, username):
        self.functions.createTaskData('BuriedTreasure', username)
        if time.time() - float(self.functions.lastRun('BuriedTreasure', username)) >= 10800:
            resp = self.neo.get('pirates/buriedtreasure/buriedtreasure.phtml?', 'https://thedailyneopets.com/dailies')
            if not self.functions.contains(resp.text, 'you have to wait another'):
                x, y = random.randint(25, 450), random.randint(45, 460)
                resp = self.neo.get('pirates/buriedtreasure/buriedtreasure.phtml?%s,%s' % (x, y), 'http://www.neopets.com/pirates/buriedtreasure/buriedtreasure.phtml?')
                gamePrize = self.functions.getBetween(resp.text, '<b><center>', '</center></b>')
                self.functions.log('Buried Treasure: %s' % gamePrize)
                self.functions.updateLastRun('BuriedTreasure', username)
