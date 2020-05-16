import json
import time
import random
from classes.functions import Functions

class Lottery:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Lottery(self, username):
        self.functions.createTaskData('Lottery', username)
        if time.time() - float(self.functions.lastRun('Lottery', username)) >= 86400:
            self.neo.get('games/lottery.phtml', 'https://thedailyneopets.com/dailies')
            for _ in range(20):
                nums = [x for x in range(1, 31)]
                random.shuffle(nums)
                resp = self.neo.post('games/process_lottery.phtml', {'one': nums[0], 'two': nums[1], 'three': nums[2], 'four': nums[3], 'five': nums[4], 'six': nums[5]}, 'http://www.neopets.com/games/lottery.phtml')
                if self.functions.contains(resp.text, 'you cannot buy any more'):
                    self.functions.log('Lottery: You can\'t buy anymore tickets')
                    break
                self.functions.log('Lottery: Purchased ticket - %s, %s, %s, %s, %s, %s' % (nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]))
            self.functions.log('Lottery: Done')
            self.functions.updateLastRun('Lottery', username)