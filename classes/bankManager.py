import time
from classes.functions import Functions

class BankManager:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def createBank(self):
        resp = self.neo.get('bank.phtml')
        currentNp = self.functions.getNp(resp.text)
        accountType = {0: 0, 1000: 1, 2500: 2, 5000: 3, 10000: 4, 25000: 5, 50000: 6, 75000: 7, 100000: 8, 250000: 9, 500000: 10, 1000000: 11, 2000000: 12, 5000000: 13, 7500000: 14, 10000000: 15}
        available = {}
        for key, value in accountType.items():
            if currentNp > key:
                available[key] = value
        bankType = list(available.keys())[-1]
        resp = self.neo.post('process_bank.phtml', {'type': 'new_account', 'name': 'x', 'add1': 'n', 'employment': 'Chia Custodian', 'salary': '10,000 NP and below', 'account_type': str(available[bankType]), 'initial_deposit': str(bankType)}, resp.url)
        if self.functions.contains(resp.text, 'Activation Code'):
            self.functions.log('Bank Manager: Your account isn\'t activated, unable to create a bank account')
        else:
            self.functions.log('Bank Manager: Created a bank account')

    def depositNp(self, np):
        resp = self.neo.get('bank.phtml')
        if self.functions.contains(resp.text, 'I see you don\'t currently have an account with us.'):
            self.createBank()
        self.neo.post('process_bank.phtml', {'type': 'deposit', 'amount': str(np)}, 'http://www.neopets.com/bank.phtml')
        self.functions.log('Bank Manager: Deposited %s NP!' % np)

    def withdrawNp(self, np, pin):
        resp = self.neo.get('bank.phtml')
        if self.functions.contains(resp.text, 'I see you don\'t currently have an account with us.'):
            self.createBank()
        if self.functions.contains(resp.text, 'Enter your'):
            self.neo.post('process_bank.phtml', {'type': 'withdraw', 'amount': str(np), 'pin': str(pin)}, 'http://www.neopets.com/bank.phtml')
        else:
            self.neo.post('process_bank.phtml', {'type': 'withdraw', 'amount': str(np)}, 'http://www.neopets.com/bank.phtml')
        self.functions.log('Bank Manager: Withdrew %s NP!' % np)

    def BankManager(self, username):
        self.functions.createTaskData('BankManager', username)
        if time.time() - float(self.functions.lastRun('BankManager', username)) >= 86400:
            resp = self.neo.get('bank.phtml')
            if self.functions.contains(resp.text, 'I see you don\'t currently have an account with us.'):
                self.createBank()
            if self.functions.contains(resp.text, 'You have already collected your interest today'):
                self.functions.log('Bank Manager: You already collected your interest today')
            elif self.functions.contains(resp.text, 'Collect Interest ('):
                interest = self.functions.getBetween(resp.text, 'allow you to gain <b>', ' NP</b> per ')
                resp = self.neo.post('process_bank.phtml', {'type': 'interest'}, resp.url)
                self.functions.log('Bank Manager: Collected %s NP interest' % interest)
            self.functions.updateLastRun('BankManager', username)