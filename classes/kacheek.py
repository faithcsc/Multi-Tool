import json
import time
import random
from classes.functions import Functions

class KacheekSeek:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def KacheekSeek(self, username):
        self.functions.createTaskData('Kacheek', username)
        if time.time() - float(self.functions.lastRun('Kacheek', username)) >= 86400:
            seek = True
            findingPlaces = [1, 2, 3, 4, 5]
            resp = self.neo.get('games/hidenseek.phtml', 'https://thedailyneopets.com/dailies')
            self.neo.get('games/hidenseek/0.phtml?xfn=', resp.url)
            while seek:
                random.shuffle(findingPlaces)
                for data in findingPlaces:
                    resp = self.neo.get('games/process_hideandseek.phtml?p=%s&game=0' % data, 'http://www.neopets.com/games/hidenseek/0.phtml?xfn=')
                    if self.functions.contains(resp.text, 'Oh... you found me'):
                        gamePrize = self.functions.getBetween(resp.text, 'You win <b>', '</b> Neopoints!!!')
                        self.functions.log('Kacheek Seek: Won %s NP!' % gamePrize)
                        break
                    if self.functions.contains(resp.text, 'Im SO BORED'):
                        self.functions.log('Kacheek Seek: Pet is bored, stopped')
                        self.functions.updateLastRun('Kacheek', username)
                        seek = False
                        break
