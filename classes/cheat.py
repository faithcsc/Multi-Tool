import time
import random
import re
from classes.functions import Functions

class Cheat:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Cheat(self, username):
        self.functions.createTaskData('Cheat', username)
        if time.time() - float(self.functions.lastRun('Cheat', username)) >= 86400:
            cardVal = 1
            resp = self.neo.get('games/cheat/index.phtml')
            resp = self.neo.post('games/cheat/cheat.phtml', None, resp.url)
            while True:
                if self.functions.contains(resp.text, ' of cheating!'):
                    currentPlayed = self.functions.getBetween(resp.text, ' played ', ' ')
                    if currentPlayed == '4':
                        cheater = self.functions.getBetween(resp.text, '"CheatYes" VALUE="', '"><BR>')
                        resp = self.neo.post('games/cheat/cheat.phtml', {'CheatYes': cheater}, resp.url)
                        if self.functions.contains(resp.text, 'NOT CHEATING!!!'):
                            cheater = self.functions.getBetween(resp.text, '<BR>but ', ' was <b>NOT')
                            self.functions.log('Accused %s of cheating, %s was not cheating' % (cheater, cheater))
                        resp = self.neo.post('games/cheat/cheat.phtml', None, resp.url)
                    else:
                        notCheating = self.functions.getBetween(resp.text, '"CheatNo" VALUE="', '">')
                        resp = self.neo.post('games/cheat/cheat.phtml', {'CheatNo': notCheating}, resp.url)
                        resp = self.neo.post('games/cheat/cheat.phtml', None, resp.url)
                if self.functions.contains(resp.text, 'You have won this round'):
                    if self.functions.contains(resp.text, 'You have beaten the hardest level'):
                        self.functions.log('Cheat AP: You won the hardest stage')
                        resp = self.neo.post('games/cheat/cheat.phtml', {'x_reset': '1'}, resp.url)
                        self.functions.updateLastRun('Cheat', username)
                        break
                    self.functions.log('Cheat AP: You won the round')
                    resp = self.neo.post('games/cheat/cheat.phtml', {'x_continue': '1'}, resp.url)
                    resp = self.neo.post('games/cheat/cheat.phtml', None, resp.url)
                elif self.functions.contains(resp.text, 'You will have to defeat'):
                    resp = self.neo.post('games/cheat/cheat.phtml', {'x_continue': '1'}, resp.url)
                    resp = self.neo.post('games/cheat/cheat.phtml', None, resp.url)
                if self.functions.contains(resp.text, 'Select Card Value'):
                    ourCards = re.findall(r'games/cards/(.*?)_', resp.text)
                    mostCommon = max(set(ourCards), key=ourCards.count)
                    ourValues = re.findall(rf'<img src=\'http://images.neopets.com/games/cards/{mostCommon}(.*?)\' height=90 width=70', resp.text)
                    das = self.functions.getBetween(resp.text, 'das1.value = \'', '\';')
                    if int(mostCommon) == 14:
                        cardData = {'jk_pc1': '', 'jk_pc2': '', 'jk_pc3': '', 'jk_pc4': '', 'das1': das, 'x_claim': '1'}
                    else:
                        cardData = {'jk_pc1': '', 'jk_pc2': '', 'jk_pc3': '', 'jk_pc4': '', 'das1': das, 'x_claim': mostCommon}
                    for data in ourValues:
                        cardData['jk_pc%s' % cardVal] = self.functions.getBetween(data, 'name=\'', '"')
                        cardVal += 1
                    cardVal = 1
                    resp = self.neo.post('games/cheat/cheat.phtml', cardData, resp.url)
                    if int(mostCommon) > 10:
                        curCard = None
                        if mostCommon == '11':
                            curCard = 'Jack'
                        elif mostCommon == '12':
                            curCard = 'Queen'
                        elif mostCommon == '13':
                            curCard = 'King'
                        elif mostCommon == '14':
                            curCard = 'Ace'
                        self.functions.log('Cheat AP: Played %s x%s' % (curCard, ourCards.count(mostCommon)))
                    else:
                        self.functions.log('Cheat AP: Played %s x%s' % (mostCommon, ourCards.count(mostCommon)))
                    resp = self.neo.post('games/cheat/cheat.phtml', None, resp.url)