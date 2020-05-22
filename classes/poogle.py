import time
import random
from datetime import datetime
from classes.functions import Functions

class PoogleRace:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def PoogleRace(self, username):
        raceTimes = ['59', '14', '29', '44']
        betTimes = ['11', '26', '41', '56']
        now = datetime.now()
        current_time = now.strftime("%M")
        self.functions.createTaskData('PoogleRace', username)
        if time.time() - float(self.functions.lastRun('PoogleRace', username)) >= 3600:
            for data in betTimes:
                if current_time == data:
                    resp = self.neo.get('faerieland/poogleracing/start.phtml')
                    winner = resp.text[-1]
                    resp = self.neo.post('faerieland/process_pooglebetting.phtml', {'poogle': winner, 'bet': '300', 'obj_info_id': '0'}, 'http://www.neopets.com/faerieland/pooglebetting.phtml')
                    if self.functions.contains(resp.url, 'thanks'):
                        self.functions.log('Poogle Race: Placed a bet on poogle #%s' % winner)
                        self.functions.updateLastRun('PoogleRace', username)
        self.functions.createTaskData('PoogleRaceFinish', username)
        if time.time() - float(self.functions.lastRun('PoogleRaceFinish', username)) >= 3600:
            for data in raceTimes:
                if current_time == data:
                    resp = self.neo.get('faerieland/poogleracing.phtml')
                    if self.functions.contains(resp.text, 'Please come back when the race starts!!!'):
                        time.sleep(60)
                        self.neo.post('faerieland/poogleracing.phtml?type=viewrace', {'rand': random.randint(1, 999)}, 'http://www.neopets.com/faerieland/poogleracing.phtml')
                        time.sleep(random.randint(5, 10))
                        resp = self.neo.post('faerieland/poogleracing.phtml', {'type': 'collect'}, 'http://www.neopets.com/faerieland/poogleracing.phtml?type=viewrace')
                        result = self.functions.getBetween(resp.text, 'You win <b>', '</b> NP back')
                        self.functions.log('Poogle Race: You won %sNP!' % result)
                        self.functions.updateLastRun('PoogleRaceFinish', username)