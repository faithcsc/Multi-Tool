import subprocess
import hashlib
import threading
import time
from classes.functions import Functions

class vars:
    output = None

class ShapeShifter(threading.Thread):
    def __init__(self, neo):
        threading.Thread.__init__(self)
        self.neo = neo
        self.x = 0
        self.y = 0
        self.input = ''
        self.numberOfShapes = 0
        self.functions = Functions()

    def getBetween(self, data, first, last):
        start = data.find(first)
        end = data.find(last, start + len(first))
        if start == -1 or end == -1:
            return -1
        else:
            return data[start + len(first):end]

    def getBetweenAll(self, data, first, last):
        list = []
        while data.find(first) != -1 and data.find(last, data.find(first) + len(first)) != 1:
            start = data.find(first)
            end = data.find(last, start + len(first))
            list.append(data[start + len(first):end])
            data = data[end + len(last):]
        return list        

    def restartGame(self):
        for _ in range(20):
            self.neo.get('medieval/process_shapeshifter.phtml?type=action&posx=2&posy=3', 'http://www.neopets.com/medieval/shapeshifter.phtml')

    def ShapeShifter(self, username):
        self.functions.createTaskData('ShapeShifter', username)
        if time.time() - float(self.functions.lastRun('ShapeShifter', username)) >= 86400:
            play = True
            while play:
                resp = self.neo.post('medieval/process_shapeshifter.phtml', {'type': 'init'}, 'http://www.neopets.com/medieval/shapeshifter_index.phtml')
                resp = self.neo.get('medieval/shapeshifter.phtml')
                level = self.getLevel(resp.text)
                self.functions.log('Shape Shifter: Working on level %s' % level)
                self.parseData(resp.text)
                solver = solvePuzzle(self.input)
                solver.run()
                if vars.output == None or vars.output[0] == '':
                    self.functions.log('Shape Shifter: Unable to solve the puzzle, getting a new puzzle..')
                    self.restartGame()
                    self.ShapeShifter(username)
                else:
                    self.functions.log('Shape Shifter: Found the solution!')
                    output = vars.output
                if output[1]:
                    movelist = [(0,0)] * self.numberOfShapes
                else:
                    movelist = eval(output[0])
                for move in movelist:
                    resp = self.neo.get('medieval/process_shapeshifter.phtml?type=action&posx=%s&posy=%s' % (move[0], move[1]), resp.url)
                    self.functions.log('Shape Shifter: Placing a piece at position %s, %s' % (move[0], move[1]))
                    if self.functions.contains(resp.text, 'You Won!'):
                        self.functions.log('Shape Shifter: You won!')
                        self.numberOfShapes = 0
                        self.input = ''
                        self.y = 0
                        self.x = 0
                    if self.functions.contains(resp.text, 'You\'ve reached your max neopoints on this game for today!'):
                        self.functions.log('Shape Shifter: You\'ve reached the daily limit')
                        play = False
                        break
            self.functions.updateLastRun('ShapeShifter', username)

    def getLevel(self, data):
        return int(self.getBetween(data, '<b><big>LEVEL ', '</big></b></center>'))

    def sendInput(self, data):
        self.input += str(data)+ ' '

    def processData(self, data):
        n = 0
        l = -1
        shape = self.getBetweenAll(data,"<tr>","</tr>")
        for i in range(len(shape)):
            shape[i] = self.getBetweenAll(shape[i],"<td","/td>")
            for j in range(len(shape[i])):
                if "<img" in shape[i][j]:
                    shape[i][j] = 1
                    n += 1
                else:
                    shape[i][j] = 0
            if l == -1:
                l = len(shape[i])
            elif l != len(shape[i]):
                self.functions.log("Shape Shifter: Shape Error")
            elif len(shape[i]) > self.x:
                self.functions.log("Shape Shifter: Shape Error")
        if len(shape) > self.y:
            self.functions.log("Shape Shifter: Shape Error")
        self.sendInput(n)
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x]:
                    self.sendInput(x + (y * self.x))

    def parseData(self, data):
        self.x = int(self.getBetween(data, 'gX = ', ';'))
        self.sendInput(self.x)
        self.y = int(self.getBetween(data, 'gY = ', ';'))
        self.sendInput(self.y)
        l = {}
        t = self.getBetween(data,"<table border=1 bordercolor='gray'>","</table>")
        t = self.getBetweenAll(t,"<td valign=top>","</td>")
        for i in range(len(t)-1,0,-1):
            if "arrow" in t[i]:
                del t[i]
        for i in range(len(t)):
            tt = self.getBetween(t[i],"http://images.neopets.com/medieval/shapeshifter/","_")
            if "GOAL" in t[i]:
                goal = i
            if tt != -1 and tt not in l:
                l[tt] = i
        bt = self.getBetween(data,"function mouseAction","}")
        bt = self.getBetweenAll(bt,'] = "','"')
        for i in range(len(bt)):
            self.sendInput(l[bt[i]])
        self.sendInput(goal)
        shapeDataList = self.getBetween(data,"ACTIVE SHAPE","<center><b><big>")
        shapeDataList = self.getBetween(shapeDataList,"<table","/table><br>")
        shapeDataList = [self.getBetween(shapeDataList,"<table","/table>")]
        if "LAST SHAPE" not in data:
            ts = self.getBetween(data,"NEXT SHAPE","<p")
            if "NEXT SHAPES" in data:
                ts = ts[ts.find("<table")+1:]
            ts = self.getBetweenAll(ts,"<table","/table>")
            shapeDataList.extend(ts)
        self.numberOfShapes = len(shapeDataList)
        self.sendInput(len(shapeDataList))
        for data in shapeDataList:
            self.processData(data)
        pass

class solvePuzzle(threading.Thread):
    def __init__(self, puzzle):
            threading.Thread.__init__(self)
            self.solver = subprocess.Popen('', executable= "classes/solver/ss", encoding='utf8', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            self.puzzle = puzzle
            self.timer = threading.Timer(3600, self.solver.kill)

    def run(self):
        try:
            self.timer.start()
            vars.output = self.solver.communicate(self.puzzle)
        finally:
            pass