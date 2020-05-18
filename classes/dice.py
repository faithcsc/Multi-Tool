import time
import random
from classes.functions import Functions

class DiceaRoo:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def DiceaRoo(self, username):
        self.functions.createTaskData('DiceaRoo', username)
        if time.time() - float(self.functions.lastRun('DiceaRoo', username)) >= 86400:
            resp = self.neo.get('games/dicearoo.phtml')
            gameHash = self.functions.getBetween(resp.text, 'ck\' value=\'', '\'>')
            resp = self.neo.post('games/play_dicearoo.phtml', {'raah': 'init', '_ref_ck': gameHash}, resp.url)
            resp = self.neo.post('games/play_dicearoo.phtml', {'type': 'start', 'raah': 'init', '_ref_ck': gameHash}, resp.url)
            while True:
                if self.functions.contains(resp.text, 'Im SO BORED of'):
                    self.functions.log('Dice-a-Roo AP: Pet is bored')
                    break
                if self.functions.contains(resp.text, 'Oh dear, that means Game Over'):
                    resp = self.neo.post('games/dicearoo.phtml', None, resp.url)
                    resp = self.neo.post('games/play_dicearoo.phtml', {'raah': 'init', '_ref_ck': gameHash}, resp.url)
                    resp = self.neo.post('games/play_dicearoo.phtml', {'type': 'start', 'raah': 'init', '_ref_ck': gameHash}, resp.url)
                if not self.functions.contains(resp.text, 'Oh dear, that means Game Over'):
                        resp = self.neo.post('games/play_dicearoo.phtml', {'raah': 'continue', '_ref_ck': gameHash}, resp.url)
                if self.functions.contains(resp.text, 'Im SO BORED of'):
                    self.functions.log('Dice-a-Roo AP: Pet is bored')
                    break
                GameDice = self.functions.getBetween(resp.text, '<br><b>', ' Dice-A-Roo</b>')
                gameResult = self.functions.getBetween(resp.text, '</td></tr><tr><td align=center><i>', '</i>').replace('<B>', '').replace('</B>', '').replace('<b>', '').replace('</b>', '').replace('  ', ' ').strip()
                self.functions.log('Dice-a-Roo AP [%s Dice]: %s' % (GameDice ,gameResult))
            self.functions.updateLastRun('DiceaRoo', username)