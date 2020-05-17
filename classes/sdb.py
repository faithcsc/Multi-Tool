import re
from classes.functions import Functions

class SDB:
    def __init__(self, neo):
        self.neo = neo
        self.functions = Functions()

    def deposit(self):
        arr = 1
        resp = self.neo.get('quickstock.phtml')
        items = "<TD align=\"left\">"
        results = resp.text.count(items)
        if results:
            item_ids = re.findall('value="(.*)"><TD', resp.text)
            data = {}
            data['buyitem'] = 0
            for item in item_ids:
                data['id_arr[%s]' % arr] = item
                data['radio_arr[%s]' % arr] = 'deposit'
                arr += 1
            data['checkall'] = 'on'
            self.neo.post('process_quickstock.phtml', data, 'http://www.neopets.com/quickstock.phtml')
            self.functions.log('SDB: Sent %s items to your SDB' % len(items))