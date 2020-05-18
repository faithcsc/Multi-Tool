import time
import re
from classes.functions import Functions

class Stocks:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def Stocks(self, username):
        self.functions.createTaskData('Stocks', username)
        if time.time() - float(self.functions.lastRun('Stocks', username)) >= 86400:
            resp = self.neo.get('stockmarket.phtml?type=list&full=true', 'http://www.neopets.com/stockmarket.phtml?type=buy')
            data = 15
            tryAgain = 15
            for _ in range(3):
                stock = list(set(re.findall(r'<b>(\w+?) %s [-\+]\d+?<\/b>' % data, resp.text)))
                if not stock:
                    tryAgain += 1
                    self.functions.log('Stock Buyer: No stocks for %s found, trying %s..' % (data, tryAgain))
                    data += 1
                if stock:
                    resp = self.neo.get('stockmarket.phtml?type=buy', 'http://www.neopets.com/stockmarket.phtml?type=list&full=true')
                    stockHash = self.functions.getBetween(resp.text, '&_ref_ck=', '\';')
                    resp = self.neo.post('process_stockmarket.phtml', {'_ref_ck': stockHash, 'type': 'buy', 'ticker_symbol': stock[0], 'amount_shares': '1000'}, 'http://www.neopets.com/stockmarket.phtml?type=buy')
                    if self.functions.contains(resp.text, 'purchase limit of 1000'):
                        self.functions.log('Stock Buyer: You can\'t buy more than 1000 shares per day')
                    elif self.functions.contains(resp.text, 'You cannot afford'):
                        self.functions.log('Stock Buyer: You don\'t have enough neopoints')
                    elif not self.functions.contains(resp.text, 'purchase limit of 1000'):
                        if not self.functions.contains(resp.text, 'You cannot afford'):
                            self.functions.log('Stock Buyer: Purchased 1000 shares of %s for %s' % (stock[0], data))
                    break
            self.functions.updateLastRun('Stocks', username)
