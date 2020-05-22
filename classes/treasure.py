import time
import random
from classes.functions import Functions

class BuriedTreasure:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def BuriedTreasure(self, username):
        self.functions.createTaskData('BuriedTreasure', username)
        if time.time() - float(self.functions.lastRun('BuriedTreasure', username)) >= 86400:
            resp = self.neo.get('pirates/buriedtreasure/buriedtreasure.phtml?', 'https://thedailyneopets.com/dailies')
            if not self.functions.contains(resp.text, 'Your account must be at least <b>24</b> hours old to play'):
                if not self.functions.contains(resp.text, 'you have to wait another'):
                    x, y = random.randint(25, 450), random.randint(45, 460)
                    resp = self.neo.get('pirates/buriedtreasure/buriedtreasure.phtml?%s,%s' % (x, y), 'http://www.neopets.com/pirates/buriedtreasure/buriedtreasure.phtml?')
                    gamePrize = self.functions.getBetween(resp.text, '<b><center>', '</center></b>')
                    self.functions.log('Buried Treasure: %s' % gamePrize)
            else:
                self.functions.log('Buried Treasure: Your account is too young to play')
            self.functions.updateLastRun('BuriedTreasure', username)