import time
from classes.functions import Functions
from classes.sdb import SDB

class SnowballAB:
    def __init__(self, neo):
        self.neo = neo
        self.sdb = SDB(self.neo)
        self.functions = Functions()

    def SnowballAB(self, username):
        self.functions.createTaskData('SnowballAB', username)
        if time.time() - float(self.functions.lastRun('SnowballAB', username)) >= 1800:
            resp = self.neo.post('faerieland/springs.phtml', {'type': 'purchase'}, 'http://www.neopets.com/faerieland/springs.phtml')
            if self.functions.contains(resp.text, 'buy one item every 30 minutes'):
                self.functions.log('Snowball AB: Can\'t Buy A Snowball Yet!')
            else:
                self.neo.get('faerieland/process_springs.phtml?obj_info_id=8429', 'http://www.neopets.com/faerieland/springs.phtml')
                self.functions.log('Snowball AB: Purchased x1 Sticky Snowball!')
                self.sdb.deposit()
            self.functions.updateLastRun('SnowballAB', username)