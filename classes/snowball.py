import time
from classes.functions import Functions
from classes.sdb import SDB

class SnowballAB:
    def __init__(self, neo):
        self.neo = neo
        self.sdb = SDB(self.neo)
        self.functions = Functions()
        self.BuyDelay = None
        self.getSettings()

    def getSettings(self):
        self.BuyDelay = int(self.functions.getSettings('BuyDelay').split(':')[1].strip())

    def SnowballAB(self, username):
        self.functions.createTaskData('SnowballAB', username)
        if self.BuyDelay < 1800:
            self.BuyDelay = 1800
        if time.time() - float(self.functions.lastRun('SnowballAB', username)) >= self.BuyDelay:
            resp = self.neo.get('faerieland/springs.phtml')
            currentNp = self.functions.getNp(resp.text)
            if currentNp >= 25:
                resp = self.neo.post('faerieland/springs.phtml', {'type': 'purchase'}, 'http://www.neopets.com/faerieland/springs.phtml')
                if self.functions.contains(resp.text, 'buy one item every 30 minutes'):
                    self.functions.log('Snowball AB: Can\'t Buy A Snowball Yet!')
                else:
                    self.neo.get('faerieland/process_springs.phtml?obj_info_id=8429', 'http://www.neopets.com/faerieland/springs.phtml')
                    self.functions.log('Snowball AB: Purchased x1 Sticky Snowball!')
                    self.sdb.deposit()
            else:
                self.functions.log('Snowball AB: You don\'t have enough neopoints to buy a snowball!')
            self.functions.updateLastRun('SnowballAB', username)
