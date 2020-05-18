import time
from classes.functions import Functions

class Wheels:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()
        
    def wheelOfExcitement(self, username):
        self.functions.createTaskData('wheelOfExcitement', username)
        if time.time() - float(self.functions.lastRun('wheelOfExcitement', username)) >= 7200:
            resp = self.neo.get('faerieland/wheel.phtml')
            if self.functions.contains(resp.text, 'already spun this wheel'):
                self.functions.log('Wheel of Excitement: Already spun this wheel')
            if not self.functions.contains(resp.text, 'already spun this wheel'):
                ref = self.functions.getBetween(resp.text, 'http://images.neopets.com/wheels', ', \'flash_')
                resp = self.neo.amf('http://www.neopets.com/amfphp/gateway.php', '\x00\x03\x00\x00\x00\x01\x00\x16WheelService.spinWheel\x00\x02/1\x00\x00\x00\t\n\x00\x00\x00\x01\x02\x00\x01%s' % '2', 'http://www.neopets.com/%s' % ref.strip())
                if self.functions.contains(resp.text, 'wheelofexcitement.gif'):
                    self.functions.log('Wheel of Excitement: Done, received the avatar')
                else:
                    self.functions.log('Wheel of Excitement: Done')
            self.functions.updateLastRun('wheelOfExcitement', username)
    
    def wheelOfMediocrity(self, username):
        self.functions.createTaskData('wheelOfMediocrity', username)
        if time.time() - float(self.functions.lastRun('wheelOfMediocrity', username)) >= 2400:
            resp = self.neo.get('prehistoric/mediocrity.phtml')
            if self.functions.contains(resp.text, 'Come back, uh, whenever'):
                self.functions.log('Wheel of Mediocrity: Already spun this wheel')
            if not self.functions.contains(resp.text, 'Come back, uh, whenever'):
                ref = self.functions.getBetween(resp.text, 'http://images.neopets.com/wheels', ', \'flash_')
                resp = self.neo.amf('http://www.neopets.com/amfphp/gateway.php', '\x00\x03\x00\x00\x00\x01\x00\x16WheelService.spinWheel\x00\x02/1\x00\x00\x00\t\n\x00\x00\x00\x01\x02\x00\x01%s' % '3', 'http://www.neopets.com/%s' % ref.strip())
                if self.functions.contains(resp.text, 'mediocrity.gif'):
                    self.functions.log('Wheel of Mediocrity: Done, received the avatar')
                else:
                    self.functions.log('Wheel of Mediocrity: Done')
            self.functions.updateLastRun('wheelOfMediocrity', username)

    def wheelOfMisfortune(self, username):
        self.functions.createTaskData('wheelOfMisfortune', username)
        if time.time() - float(self.functions.lastRun('wheelOfMisfortune', username)) >= 7200:
            resp = self.neo.get('halloween/wheel/index.phtml')
            if self.functions.contains(resp.text, 'Come back later'):
                self.functions.log('Wheel of Misfortune: Already spun this wheel')
            if not self.functions.contains(resp.text, 'Come back later'):
                ref = self.functions.getBetween(resp.text, 'http://images.neopets.com/wheels', ', \'flash_')
                resp = self.neo.amf('http://www.neopets.com/amfphp/gateway.php', '\x00\x03\x00\x00\x00\x01\x00\x16WheelService.spinWheel\x00\x02/1\x00\x00\x00\t\n\x00\x00\x00\x01\x02\x00\x01%s' % '4', 'http://www.neopets.com/%s' % ref.strip())
                self.functions.log('Wheel of Misfortune: Done')
            self.functions.updateLastRun('wheelOfMisfortune', username)

    def wheelOfKnowledge(self, username):
        self.functions.createTaskData('wheelOfKnowledge', username)
        if time.time() - float(self.functions.lastRun('wheelOfKnowledge', username)) >= 86400:
            resp = self.neo.get('medieval/knowledge.phtml')
            if self.functions.contains(resp.text, 'already spun this wheel'):
                self.functions.log('Wheel of Knowledge: Already spun this wheel')
            if not self.functions.contains(resp.text, 'already spun this wheel'):
                ref = self.functions.getBetween(resp.text, 'http://images.neopets.com/wheels', ', \'flash_')
                resp = self.neo.amf('http://www.neopets.com/amfphp/gateway.php', '\x00\x03\x00\x00\x00\x01\x00\x16WheelService.spinWheel\x00\x02/1\x00\x00\x00\t\n\x00\x00\x00\x01\x02\x00\x01%s' % '1', 'http://www.neopets.com/%s' % ref.strip())
                if self.functions.contains(resp.text, 'brightvale.gif'):
                    self.functions.log('Wheel of Knowledge: Done, received the avatar')
                else:
                    self.functions.log('Wheel of Knowledge: Done')
            self.functions.updateLastRun('wheelOfKnowledge', username)

    def wheelOfExtravagance(self, username):
        self.functions.createTaskData('wheelOfExtravagance', username)
        if time.time() - float(self.functions.lastRun('wheelOfExtravagance', username)) >= 86400:
            resp = self.neo.get('desert/extravagance.phtml')
            if self.functions.contains(resp.text, 'already spun the wheel today'):
                self.functions.log('Wheel of Extravagance: Already spun this wheel')
            if not self.functions.contains(resp.text, 'already spun the wheel today'):
                ref = self.functions.getBetween(resp.text, 'http://images.neopets.com/wheels', ', \'flash_')
                resp = self.neo.amf('http://www.neopets.com/amfphp/gateway.php', '\x00\x03\x00\x00\x00\x01\x00\x16WheelService.spinWheel\x00\x02/1\x00\x00\x00\t\n\x00\x00\x00\x01\x02\x00\x01%s' % '6', 'http://www.neopets.com/%s' % ref.strip())
                if self.functions.contains(resp.text, 'extravagance.gif'):
                    self.functions.log('Wheel of Extravagance: Done, received the avatar')
                else:
                    self.functions.log('Wheel of Extravagance: Done')
            self.functions.updateLastRun('wheelOfExtravagance', username)

    def wheelOfMonotony(self, username):
        self.functions.createTaskData('monotonystart', username)
        if time.time() - float(self.functions.lastRun('monotonystart', username)) >= 86400:
            self.functions.createTaskData('monotony1', username)
            if time.time() - float(self.functions.lastRun('monotony1', username)) >= 86400:
                resp = self.neo.get('prehistoric/monotony/monotony.phtml')
                if self.functions.contains(resp.text, 'already spun'):
                    self.functions.log('Wheel of Monotony: Already spun this wheel')
                if not self.functions.contains(resp.text, 'already spun'):
                    ref = self.functions.getBetween(resp.text, 'http://images.neopets.com/wheels', ', \'flash_')
                    resp = self.neo.amf('http://www.neopets.com/amfphp/gateway.php', '\x00\x03\x00\x00\x00\x01\x00\x1aWheelService.startMonotony\x00\x02/1\x00\x00\x00\x05\x0a\x00\x00\x00\x00', 'http://www.neopets.com/%s' % ref.strip())
                    self.functions.log('Wheel of Monotony: Started spinning the wheel, checking back in 2 hours')
                self.functions.updateLastRun('monotony1', username)
                self.functions.createTaskData('monotonycollect', username)
                self.functions.updateLastRun('monotonycollect', username)
            if time.time() - float(self.functions.lastRun('monotonycollect', username)) >= 7200:
                ref = self.functions.getBetween(resp.text, 'http://images.neopets.com/wheels', ', \'flash_')
                resp = self.neo.amf('http://www.neopets.com/amfphp/gateway.php', '\x00\x03\x00\x00\x00\x01\x00\x16WheelService.spinWheel\x00\x02/1\x00\x00\x00\t\n\x00\x00\x00\x01\x02\x00\x01%s' % '5', 'http://www.neopets.com/%s' % ref.strip())
                if self.functions.contains(resp.text, 'monotony.gif'):
                    self.functions.log('Wheel of Monotony: Done, received the avatar')
                else:
                    self.functions.log('Wheel of Monotony: Done')
                self.functions.updateLastRun('monotonystart', username)
                self.functions.updateLastRun('monotonycollect', username)
