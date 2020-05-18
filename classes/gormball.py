import time
import random
from classes.functions import Functions

class Gormball:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Gormball(self, username):
        self.functions.createTaskData('Gormball', username)
        if time.time() - float(self.functions.lastRun('Gormball', username)) >= 86400:
            resp = self.neo.get('space/gormball.phtml')
            gameHash = self.functions.getBetween(resp.text, '\'xcn\' value=\'', '\'>')
            resp = self.neo.post('space/gormball2.phtml', {'xcn': gameHash, 'player_backed': random.randint(1, 8)}, resp.url)
            while True:
                if self.functions.contains(resp.text, 'Im SO BORED of'):
                    self.functions.log('Gormball AP: Pet is bored')
                    break
                lastCharacter = self.functions.getBetween(resp.text, '_character\' value=\'', '\'>')
                pageCount = self.functions.getBetween(resp.text, '_count\' value=', '><')
                if lastCharacter == 'You':
                    resp = self.neo.post('space/gormball2.phtml', {'type': 'moveon', 'page_count': pageCount, 'xcn': gameHash, 'turns_waited': '1', 'last_character': lastCharacter}, resp.url)
                    if self.functions.contains(resp.text, '<b>You are the last remaining character!!! You have won!!!</b>'):
                        self.functions.log('Gormball AP: You Won!')
                        resp = self.neo.get('space/gormball.phtml', resp.url)
                        resp = self.neo.post('space/gormball2.phtml', {'xcn': gameHash, 'player_backed': random.randint(1, 8)}, resp.url)
                elif lastCharacter != 'You':
                    resp = self.neo.post('space/gormball2.phtml', {'type': 'moveon', 'page_count': pageCount, 'xcn': gameHash, 'last_character': lastCharacter}, resp.url)
                    if self.functions.contains(resp.text, '<b>You are the last remaining character!!! You have won!!!</b>'):
                        self.functions.log('Gormball AP: You Won!')
                        resp = self.neo.get('space/gormball.phtml', resp.url)
                        resp = self.neo.post('space/gormball2.phtml', {'xcn': gameHash, 'player_backed': random.randint(1, 8)}, resp.url)
                if self.functions.contains(resp.text, 'Oh dear, you are out of the game'):
                    scoredPoints = self.functions.getBetween(resp.text, 'You scored <b>', '</b> points!')
                    self.functions.log('Gormball AP: Game Over - You scored %s points' % scoredPoints)
                    resp = self.neo.get('space/gormball.phtml', resp.url)
                    resp = self.neo.post('space/gormball2.phtml', {'xcn': gameHash, 'player_backed': random.randint(1, 8)}, resp.url)
                if self.functions.contains(resp.text, 'The Gormball explodes on '):
                    gormballExplodes = self.functions.getBetween(resp.text, 'The Gormball explodes on ', '!!!</b>')
                    self.functions.log('Gormball AP: The Gormball explodes on %s' % gormballExplodes)
                    pageCount = self.functions.getBetween(resp.text, '_count\' value=', '><')
                    resp = self.neo.post('space/gormball2.phtml', {'xcn': gameHash, 'type': 'moveon', 'page_count': pageCount}, resp.url)
                if self.functions.contains(resp.text, 'Im SO BORED of'):
                    self.functions.log('Gormball AP: Pet is bored')
                    break
            self.functions.updateLastRun('Gormball', username)