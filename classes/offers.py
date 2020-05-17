import time
import random
from classes.functions import Functions

class RichSlorg:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def RichSlorg(self, username):
        self.functions.createTaskData('RichSlorg', username)
        if time.time() - float(self.functions.lastRun('RichSlorg', username)) >= 86400:
            self.neo.get('shop_of_offers.phtml?slorg_payout=yes', 'https://thedailyneopets.com/dailies')
            self.functions.log('Rich Slorg: Done')
            self.functions.updateLastRun('RichSlorg', username)