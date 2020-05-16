import json
import time
from classes.functions import Functions

class Trudy:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Trudy(self, username):
        self.functions.createTaskData('Trudy', username)
        if time.time() - float(self.functions.lastRun('Trudy', username)) >= 86400:
            resp = self.neo.get('trudys_surprise.phtml?delevent=yes', 'https://www.jellyneo.net/?go=dailies')
            if self.functions.contains(resp.text, '&slt=1'):
                result = self.functions.getBetween(resp.text, 'phtml?id=', '" name="')
                resp = self.neo.get('trudydaily/slotgame.phtml?id=%s' % result, resp.url)
                results = self.functions.getBetween(resp.text, '\'key\': \'', '\'};')
                resp = self.neo.post('trudydaily/ajax/claimprize.php', {'action': 'getslotstate', 'key': results}, 'http://www.neopets.com/trudydaily/slotgame.phtml?id=%s' % result)
                resp = self.neo.post('trudydaily/ajax/claimprize.php', {'action': 'beginroll'}, resp.url)
                self.neo.post('trudydaily/ajax/claimprize.php', {'action': 'prizeclaimed'}, resp.url)
                self.functions.log('Trudy\'s Surprise: Done')
                self.functions.updateLastRun('Trudy', username)
            else:
                self.functions.log('Trudy\'s Surprise: Already done today')
