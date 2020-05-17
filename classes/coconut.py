import time
import random
from classes.functions import Functions

class CoconutShy:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def CoconutShy(self, username):
        self.functions.createTaskData('CoconutShy', username)
        if time.time() - float(self.functions.lastRun('CoconutShy', username)) >= 86400:
            resp = self.neo.get('halloween/coconutshy.phtml', 'https://thedailyneopets.com/dailies')
            if self.functions.contains(resp.text, 'Come back tomorrow'):
                self.functions.updateLastRun('CoconutShy', username)
                return
            ref = self.functions.getBetween(resp.text, 'new SWFObject(\'http://images.neopets.com/halloween/', '\',')
            for _ in range(20):
                resp = self.neo.post('halloween/process_cocoshy.phtml?coconut=1&r=%s' % random.randint(20000, 99999), {'onData': '[type Function]'}, ref)
                result = self.functions.getBetween(resp.text, '&error=', '%21')
                if self.functions.contains(resp.text, '%2C'):
                    self.functions.log('Coconut Shy: %s' % result.replace('+', ' ').replace('%2C', ''))
                else:
                    self.functions.log('Coconut Shy: %s' % result.replace('+', ' '))
            self.functions.updateLastRun('CoconutShy', username)