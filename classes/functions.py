import os
import time
import in_place

class Functions:
    def getBetween(self, data, first, last):
        return data.split(first)[1].split(last)[0]

    def log(self, message):
        print(time.strftime('%A') + ' ' + '%s%s' % (time.strftime('%H:%M:%S => '), message.encode('utf-8').decode('utf-8')))

    def contains(self, data, string):
        return True if string in data else False

    def getNp(self, data):
        _points = self.getBetween(data, '<a id=\'npanchor\' href="/inventory.phtml">', '</a> <span </a> <span ')
        if self.contains(_points, ','): _points = _points.replace(',', '')
        return int(_points)

    def bankBal(self, data):
        return self.getBetween(data, '<td bgcolor=\'#ffffff\'><b>', ' NP</b></td>') if self.contains(data, '<b>Your Current Balance:</b>') else False

    def lastRun(self, task, user):
        with open('data/%s.dat' % user, 'r') as f:
            for data in f:
                if data.strip().split(':')[0] == task:
                    return data.strip().split(':')[1]

    def createTaskData(self, task, user):
        if not os.path.exists('data/%s.dat' % user):
            with open('data/%s.dat' % user, 'w') as f:
                f.write('')
        with open('data/%s.dat' % user, 'r') as f:
            data = f.read()
        with open('data/%s.dat' % user, 'a') as f:
            if not self.contains(data, task):
                f.write('%s:0\n' % task)

    def updateLastRun(self, task, timestamp, user):
        lastRun = self.lastRun(task, user)
        with in_place.InPlace('data/%s.dat' % user) as f:
            for data in f:
                data = data.replace('%s:%s' % (task, lastRun), '%s:%s' % (task, time.time()))
                f.write(data)
