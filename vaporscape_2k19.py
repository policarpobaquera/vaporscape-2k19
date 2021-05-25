# VAPORSCAPE
# 15-112 Term Project
# Fall 2019
# version. TP3
#
# by Policarpo del Canto Baquera
# pdelcant

from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random

# Background music only available for Windows OS
try: 
    import winsound
    print('\nYou are listening to Macintosh Plus - Floral Shoppe '+\
            '- 02 リサフランク420 - 現代のコンピュー .\n')
except: 
    print('\nBackground music (Macintosh Plus) not available '+\
        'on Macintosh Computers.\n') 

class Vaporscape(ModalApp):
    # Based on: http://www.cs.cmu.edu/~112/notes/notes-animations-part2
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.game = Game()
        app.gameOver = GameOver()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 70

class Color(object):
    # Color manager class
    # Fixed colors
    c1 = 'sky blue'     # Light blue
    c2 = 'white'        # Text (white)
    c3 = 'gray'         # Grays
    c4 = 'spring green' # Text (green)
    c5 = 'white smoke'  # Text (white)
    c6 = 'deep pink'    # Text (pink)
    c7 = 'blue'         # Text (blue)
    c8 = 'medium blue'  # Special Mode
    # List of Dynamic Colors
    dynamicColors = []

    def __init__(self, rgb0, rgb1):
        self.rgb0 = rgb0
        self.rgb1 = rgb1
        self.current = list(rgb0)
        self.RGB = self.getRGBCode(self.current)
        Color.dynamicColors.append(self)
    
    def getRGBCode(self, rgb):
        RGBCode = '#%02x%02x%02x' % tuple(rgb)
        return RGBCode

    @staticmethod
    def change():
        # A function that changes the dynamic colors of the game from one
        # initial value to a second value through time.
        changeRate = 2
        for col in Color.dynamicColors:
            for i in range(3):
                if (col.rgb0[i] > col.rgb1[i]):
                    if col.current[i] > col.rgb1[i]:
                        col.current[i] -= changeRate
                elif (col.rgb0[i] < col.rgb1[i]):
                    if col.current[i] < col.rgb1[i]:
                        col.current[i] += changeRate
            col.RGB = col.getRGBCode(col.current)

class SplashScreenMode(Mode):
    # Based on: http://www.cs.cmu.edu/~112/notes/notes-animations-part2
    def appStarted(mode):
        mode.timer = 0
        mode.cdInt = Color((255, 146, 149), (15,  6, 104))
        mode.cdIntInv = Color((15,  6, 104), (255, 146, 149))
        # Background music
        try:
            winsound.PlaySound('macintosh plus.wav', winsound.SND_ASYNC)
        except:
            pass

    def timerFired(mode):
        mode.timer += 2
        Color.change()

    def keyPressed(mode, event):
        mode.app.game = Game()
        mode.app.gameOver = GameOver()
        mode.app.setActiveMode(mode.app.game)

    def redrawAll(mode, canvas):
        w, h = mode.width, mode. height
        canvas.create_rectangle(0, 0, w, h, fill = mode.cdInt.RGB)
        times = mode.timer
        if (times > 400):
            times = 400
        for i in range(mode.timer):
            canvas.create_text((w/2)+i, (h/2)+i, 
                text = 'V A P O R S C A P E', font = 'system 50 italic',
                fill = mode.cdIntInv.RGB)
        canvas.create_text(w//2, h//2, 
            text = 'V A P O R S C A P E', font = 'system 50 italic',
            fill = Color.c5)
        canvas.create_text(w//2, h//2 + 80, 
            text = 'press any key to start', font = 'system 17',
            fill = mode.cdInt.RGB)
        
class GameOver(Mode):
    # Based on: http://www.cs.cmu.edu/~112/notes/notes-animations-part2
    def appStarted(mode):
        mode.cd = Color((15,  6, 104), (255, 146, 149))
        mode.score = mode.app.game.score
        mode.name = 'anonymous'
        mode.ranking = False
        mode.rankingList = []
        mode.now = str(datetime.datetime.now())

    def timerFired(mode):
        Color.change()
    
    def keyPressed(mode, event):
        if (mode.ranking == False):
            name = mode.getUserInput('What is your name?')
            if (name != '' and name != None):
                mode.name = name
            mode.writeRank()
            mode.readRank()
            mode.ranking = True
        else:
            mode.app.splashScreenMode = SplashScreenMode()
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def writeRank(mode):
        # The score and name of the player are stored in the ranking.txt file
        ranking = open('ranking.txt', 'a')
        ranking.write(f'\n{mode.score}~{mode.name}~{mode.now}')
        ranking.close()

    def readRank(mode):
        # This function generates a sorted list of all the scores stored in the 
        # ranking.txt file
        ranking = open('ranking.txt','r')
        rankingList = ranking.readlines()
        for rank in rankingList:
            rankPos = []
            i = 0
            for s in rank.strip().split('~'):
                i += 1
                if (i == 1):
                    rankPos.append(int(s))
                else:
                    rankPos.append(s)
            mode.rankingList.append(tuple(rankPos))
        mode.rankingList.sort()
        if (len(mode.rankingList) < 5):
            for _ in range(5 - len(mode.rankingList)):
                emptyRank = ('----', '----', '2016-12-02 17:58:11.148822')
                mode.rankingList.insert(0, emptyRank)
        ranking.close()

    def redrawAll(mode, canvas):
        w, h = mode.width, mode. height
        canvas.create_rectangle(0, 0, w, h, fill = mode.cd.RGB)
        if (mode.ranking == False):
            canvas.create_text(w//2, h//2 - 80, 
                text = 'Your score:', font = 'system 17',
                fill = Color.c5)
            canvas.create_text(w//2, h//2, text = f'{mode.score} points', 
                font = 'system 50', fill = Color.c5)
            canvas.create_text(w//2, h//2 + 80, 
                text = 'Congratulations!', font = 'system 17',
                fill = Color.c5)
            canvas.create_text(w//2, h//2 + 250, 
                text = 'press any key to access the ranking', 
                font = 'system 17', fill = Color.c5)
        else:
            position = 130
            length = len(mode.rankingList)
            place = 0
            for rank in range(length-1, length-6, -1):
                place += 1
                color = Color.c5
                score = mode.rankingList[rank][0]
                name = mode.rankingList[rank][1]
                time = mode.rankingList[rank][2]
                position += 60
                if (time == mode.now):
                    color = Color.c4
                canvas.create_text(230, position, text = place, 
                    font = 'system 30',fill = color, anchor = 'w') 
                canvas.create_text(w//2 + 50, position, text = f'{score}', 
                    font = 'system 30',fill = color, anchor = 'e')
                canvas.create_text(w//2 + 80, position, text = f'{name}', 
                    font = 'system 30',fill = color, anchor = 'w')
            canvas.create_text(w//2 + 50, 120, text = 'ranking :', 
            font = 'system 17', fill = Color.c5, anchor = 'e')
            canvas.create_text(w//2, h//2 + 250, 
                text = 'press any key to restart the game', font = 'system 17',
                fill = Color.c5)

class Game(Mode):
    # Based on: http://www.cs.cmu.edu/~112/notes/notes-animations-part2
    @staticmethod
    def getSprites(image, spritesNo, coord):
        # Returns a list of sprites
        sprites = [ ]
        for i in range (spritesNo):
            # 'coord' is a tuple with the coordinates of each sprite
            x0, y0, x1, y1 = coord
            cropCoord = (x0 + (x1-x0)*i, y0, x0 + (x1-x0)*(i+1), y1)
            sprite = image.crop(cropCoord)
            sprites.append(sprite)
        return sprites

    def appStarted(mode):
        # Initial parameters
        mode.gameOver = False
        mode.timer = 0
        mode.score = 0
        # Dynamic Colors
        mode.cd1 = Color((255, 146, 149), (19,  0, 79)) # Sky
        mode.cd2 = Color((238, 238,   0), (235, 1, 150)) # Sun
        mode.cd3 = Color((255,  50, 144), (15,  6, 104)) # Ground
        mode.skyC = mode.cd1.RGB
        mode.sunC = mode.cd2.RGB
        mode.groundC = mode.cd3.RGB
        # Time Length indicates the duration of the game
        mode.timeLength = 0.6
        # Background
        mode.checkerboard = Checkerboard(mode)
        mode.mountains = Mountains(mode)
        mode.sun = Sun(mode)
        # Player
        mode.player = Player(mode)
        mode.jumping = False
        # Objects manager
        mode.objects = Objects(mode)
        # Objects in game
        gameSet = copy.copy(mode.gameCreation())
        mode.gameSet = mode.checkPlayability(gameSet)
        # Collision parameters
        mode.crash = False
        mode.crashTime = None
        # Special Mode
        mode.specialMode = False
        mode.specialTime = None

    def gameCreation(mode):
        # Generates a game from scratch placing heads, coins and spaces
        # randomly in the table allowing the player to always have an accesible
        # path to run
        lengthOfGame = 60 
        tracks = 4 # Track 0, 1, 2, 3
        # List of Objects in the game
        empty, head, coin, win95 = 0, 1, 2, 3
        objList = [empty, head, coin]
        # All games end with the same ending sequence for aesthetic reasons
        game = []
        endSequence = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
                    [1, 0, 0, 1], [0, 0, 0, 0]]
        game += endSequence
        # Game Generation
        win95Counter = 1
        win95Line = random.randint(20,30)
        win95Track = random.randint(0, 3)
        lineNo = 0
        for i in range(lengthOfGame):
            lineNo += 1
            headCounter = 3
            gameLine = []
            for j in range(4): 
                if (headCounter > 0):
                    obj = random.choice(objList)
                    if (obj == head):
                        headCounter -= 1                   
                else:
                    obj = random.choice([empty, coin])
                gameLine.append(obj)
            if (lineNo == win95Line):
                gameLine[win95Track] = win95
            game.append(gameLine)
        return game

    def checkPlayability(mode, game, line = -1, track = None):
        # Checks recursively every line in the track for heads that block a 
        # linear run of the player.
        # Ex.   h1  -   -   -
        #       -   h2  h3  h4 
        #       -   -   -   -
        # h1 (head1) is removed to break the barrier created by h2, h3 and h4.
        empty, head, coin, win95 = 0, 1, 2, 3
        lengthOfGame = 60 
        if (line == -lengthOfGame):
            return game
        elif (game[line][0] != head) and (game[line][1] != head) and \
             (game[line][2] != head) and (game[line][3] != head):
                return mode.checkPlayability(game, line-1, None)
        elif (track == None):
            trackList = [0, 1, 2, 3]
            random.shuffle(trackList)
            for track in trackList:
                if (game[line][track] != head):
                    return mode.checkPlayability(game, line-1, track)
        else:
            if (game[line][track] == head):
                game[line][track] = random.choice([empty, coin])
            return mode.checkPlayability(game, line-1, track)

    def gameInterpreter(mode):
        # Reads the tuples of a list and creates objects depending on the 
        # pattern of the tuple. 0 = Empty / 1 = Head / 2 = Coin
        if (len(mode.gameSet) != 0):
            # The interpreter creates the objects in tracks 1 and 2 first 
            # for later drawing purpouses (perspective)
            for i in [1, 2, 0, 3]:
                if (mode.gameSet[-1][i] == 1):    Head(mode, i)
                elif (mode.gameSet[-1][i] == 2):  Coin(mode, i)
                elif (mode.gameSet[-1][i] == 3):  Win95(mode, i)
            mode.gameSet.pop()

    def timerFired(mode):
        if (mode.gameOver == False):
            mode.timer += 1
            # Color changing
            if (mode.timer % 3 == 0):
                Color.change()
            # The game ends when the sun is completely set
            if (mode.sun.y0 > mode.height//2):
                mode.gameOver = True
            # Checkerboard animation
            if (mode.sun.y0 < (mode.height//2)-50):
                if (mode.timer % 3 == 0) and (mode.timer % 6 != 0):
                    mode.checkerboard.create(0)
                elif (mode.timer % 6  == 0):
                    mode.checkerboard.create(1)
            mode.checkerboard.move()
            # Mountains animation
            if (mode.timer % 4 == 0):
                mode.mountains.create()
            mode.mountains.move()
            # Sun animation
            randomTrigger = random.choice([5,12])
            if (mode.timer % randomTrigger == 0):
                mode.sun.create()
            mode.sun.move()
            # Player animation
            if (mode.jumping == False):
                sprNo = len(mode.player.sprites)
                mode.player.currentSpr = (1 + mode.player.currentSpr) % sprNo
            # Collision of objects
            mode.checkCollision()
            if (mode.crash == True) and (mode.crashTime == None):
                mode.crashTime = mode.timer
            if (mode.crashTime != None) and (mode.timer - mode.crashTime == 8):
                mode.crashTime = None
                mode.crash = False
            # Object generation
            if (mode.timer % 5 == 0):
                mode.gameInterpreter()
            # Object animation
            if (mode.timer % 1 == 0):
                mode.objects.move()
            # Special Mode (win95)
            if (mode.specialMode == True) and (mode.specialTime == None):
                mode.specialTime = mode.timer
            if (mode.specialTime != None) and \
                (mode.timer - mode.specialTime == 70):
                mode.specialMode = False
            if (mode.specialMode == True):
                mode.skyC = Color.c8
                mode.sunC = Color.c2
                mode.groundC = Color.c8
            elif (mode.specialMode == False):
                mode.skyC = mode.cd1.RGB
                mode.sunC = mode.cd2.RGB
                mode.groundC = mode.cd3.RGB         

    def keyPressed(mode, event):
        if  (event.key == 'Left'): 
            mode.jumping = True
            mode.player.currentSpr = 0
            mode.player.move(-1)
        if (event.key == 'Right'): 
            mode.jumping = True
            mode.player.currentSpr = 1
            mode.player.move(+1)
        if (mode.gameOver == True):
            if (mode.checkScoreZero() == True):
                mode.app.splashScreenMode.playing = False
                mode.app.splashScreenMode = SplashScreenMode()
                mode.app.setActiveMode(mode.app.splashScreenMode)
            else:
                mode.app.setActiveMode(mode.app.gameOver)
    
    def keyReleased(mode, event):
        mode.jumping = False

    def checkCollision(mode):
        for i in range(len(mode.objects.lst)):
            obj = mode.objects.lst
            if (obj[i].y > 90) and (type(obj[i]) == Head) and \
               (obj[i].pos == mode.player.pos):
                    if (mode.specialMode == True):
                        mode.score += 200
                    else:
                        mode.score -= 200
                    mode.crash = True
                    mode.checkScoreZero()
                    obj[i].sprite = obj[i].broken
            elif (obj[i].y > 100) and (type(obj[i]) == Coin) and \
                 (obj[i].pos == mode.player.pos):
                    mode.score += 50
                    obj[i].catch = True
            elif (obj[i].y > 120) and (type(obj[i]) == Win95) and \
                 (obj[i].pos == mode.player.pos):
                    mode.specialMode = True

    def checkScoreZero(mode):
        if (mode.score <= 0):
            mode.gameOver = True
            return True
        else:
            return False

    def redrawAll(mode, canvas):
        w = mode.width
        h = mode.height
        # Coordinates origin
        oX = w//2
        oY = h//2
        # Background
        canvas.create_rectangle(0, 0, w, h, fill = mode.skyC) # Sky
        mode.sun.draw(canvas)
        canvas.create_rectangle(0, oY, w, h, fill = mode.groundC, width = 0)
        if (mode.specialMode == False):
            mode.checkerboard.draw(canvas)
        mode.mountains.draw(canvas)
        # Objects
        mode.objects.draw(canvas)
        # Player
        if (mode.gameOver == False):
            mode.player.draw(canvas)
        # Score
        score = str(mode.score)
        if (mode.score >= 0):
            extra0 = (4 - len(score))*'0'
            scoreVal = f'{extra0}{score}'
        else:
            scoreVal = f'{score}'
        if (mode.specialMode == False):
            scoreColor = Color.c7
            # Red score if collision happens
            if (mode.crash == True):
                scoreColor = Color.c6
        elif (mode.specialMode == True):
            scoreColor = Color.c2
            # Green score if collision happens when specialMode is activated
            if (mode.crash == True):
                scoreColor = Color.c4
        canvas.create_text(oX, 32, text = scoreVal,
            font = 'system 27', fill = scoreColor)
        # Special Mode
        if (mode.specialMode == True):
            canvas.create_rectangle(60, 60, w-60, h-60, 
                outline = Color.c2, width = 2)
            m = 'An exception has ocurred. This was called from Win95 logo.\n'+\
               'It may be possible to continue the game normally. Although,\n'+\
               'now you can collide with any marble head and get points.'
            canvas.create_text(oX, h - 120, text = m,
                font = 'system 16', fill = Color.c2, justify = LEFT)
        # GameOver message
        if (mode.gameOver == True):
            if (mode.checkScoreZero() == True):
                msg0 = 'You fell below zero'
                msg1 = 'press any key to restart'
                color = Color.c2
            else:
                msg0 = 'Time\'s up'
                msg1 = 'press any key to continue'
                color = Color.c7
            canvas.create_text(oX, oY - oY//2, text = msg0, 
                    font = 'system 50', fill = color)
            canvas.create_text(oX, h - 50, text = msg1, 
                    font = 'system 20', fill = color)
           
class Sun(Game):
    def __init__(self, app):
        self.app = app
        margin = 30
        shift = 30
        self.x0 = (self.app.width - (self.app.height - 2*margin))//2
        self.y0 = margin + shift
        self.x1 = self.app.width - self.x0
        self.y1 = self.app.height - margin + shift
        self.scale = 0.1
        self.set = self.app.timeLength
        # Every sunLine is stored in a set()
        self.sunLines = set()

    def create(self):
        newSunLine = SunLine(self.app)
        self.sunLines.add(newSunLine)

    def move(self):
        # The sun moves down and gets bigger simultaneously
        self.x0 += self.scale
        self.y0 += self.scale + self.set
        self.x1 -= self.scale
        self.y1 -= self.scale - self.set
        # The sunLines move down continuously and when they reach the horizon
        # they are removed from the animation
        remove = None
        for sunLine in self.sunLines:
            sunLine.move()
            if (sunLine.y > self.app.height//2):
                remove = sunLine
        if (remove != None):
            self.sunLines.remove(remove)
            remove = None
        
    def draw(self, canvas):
        canvas.create_oval(self.x0, self.y0, self.x1, self.y1, 
            width = 0, fill = self.app.sunC)
        for sunLine in self.sunLines:
            canvas.create_line(0, sunLine.y, self.app.width, sunLine.y, 
                fill = self.app.skyC, width = sunLine.width)

class SunLine(Sun):
    def __init__(self, app):
        self.app = app
        self.y = self.app.sun.y0
        self.width = 0

    def move(self):
        self.y += 2
        self.width += 0.1

class Checkerboard(Game):
    # Initial value for gray color
    shade = 80
    def __init__(self, app):
        self.app = app
        # Every cell in the checkerboard is stored in a animated set()
        self.bars = set()

    def create(self, pattern):
        newBar = Bar(self.app, pattern)
        self.bars.add(newBar)
    
    def move(self):
        # When a bar reach the canvas limit is removed
        remove = None
        for bar in self.bars:
            bar.move()
            if (bar.yA > self.app.height):
                remove = bar
        if (remove != None):
            self.bars.remove(remove)
            remove = None

    def draw(self, canvas):
        for bar in self.bars:
            bar.draw(canvas)

class Bar(Checkerboard):
    def __init__(self, app, pattern):
        self.app = app
        self.pattern = pattern
        self.dyA = 10
        self.yA = self.app.height//2
        self.dyB = 0
        self.yB = self.yA + self.dyB
        self.coordinates(self.yA, self.yB)
        self.color = Checkerboard.shade

    def coordinates(self, yA, yB):
        yA, yB = yA-self.app.height//2, yB-self.app.height//2
        oX = self.app.width//2
        # Each coordinate of the animated checkerboard is calculated as a point
        # in one of the lines that connect the center of the canvas to a point
        # in the bottom border of the canvas.
        self.xA1, self.xB1 = oX-2*yA, oX-2*yB
        self.xA2, self.xB2 = oX-(4/3)*yA, oX-(4/3)*yB
        self.xA3, self.xB3 = oX-(2/3)*yA, oX-(2/3)*yB
        self.xA4, self.xB4 = oX, oX
        self.xA5, self.xB5 = oX+(2/3)*yA, oX+(2/3)*yB
        self.xA6, self.xB6 = oX+(4/3)*yA, oX+(4/3)*yB
        self.xA7, self.xB7 = oX+2*yA, oX+2*yB

    def move(self):
        # The upper coordinates of each cell move proportionally with the 
        # timer. The distance between the upper and bottom coordinates grow
        # with the timer call which produce the effect of the objects being 
        # bigger when they get close to the player position.
        self.yA += self.dyA
        self.dyB += 2
        self.yB = self.yA + self.dyB 
        self.coordinates(self.yA, self.yB)
        self.color -= 3
        if (self.color < 0):
            self.color = 0

    def draw(self, canvas):
        color = f'{Color.c3}{self.color}'
        if (self.pattern == 0):
            canvas.create_polygon(self.xA1, self.yA, self.xA2, self.yA, 
                self.xB2, self.yB, self.xB1, self.yB, fill = color)
            canvas.create_polygon(self.xA3, self.yA, self.xA4, self.yA, 
                self.xB4, self.yB, self.xB3, self.yB, fill = color)
            canvas.create_polygon(self.xA5, self.yA, self.xA6, self.yA, 
                self.xB6, self.yB, self.xB5, self.yB, fill = color)
        else:
            canvas.create_polygon(self.xA2, self.yA, self.xA3, self.yA, 
                self.xB3, self.yB, self.xB2, self.yB, fill = color)
            canvas.create_polygon(self.xA4, self.yA, self.xA5, self.yA, 
                self.xB5, self.yB, self.xB4, self.yB, fill = color)
            canvas.create_polygon(self.xA6, self.yA, self.xA7, self.yA, 
                self.xB7, self.yB, self.xB6, self.yB, fill = color)

class Mountains(Game):
    def __init__(self, app):
        self.app = app
        # Every summit in the mountains is stored in a animated set()
        self.summits = set()
    
    def create(self):
        initialY = random.randint(1, 5)
        side = random.choice(['left', 'right'])
        newSummit = Summit(self.app, initialY, side)
        self.summits.add(newSummit)

    def move(self):
        # When a summit reach the canvas limit is removed
        remove = None
        for summit in self.summits:
            summit.move()
            if (summit.xA > self.app.width) or (summit.xC < 0):
                remove = summit
        if (remove != None):
            self.summits.remove(remove)
            remove = None
    
    def draw(self, canvas):
        for summit in self.summits:
            summit.draw(canvas)

class Summit(Mountains):
    def __init__(self, app, initialY, side):
        self.app = app
        self.side = side
        # Every summit is defined by three points: a, b and c
        self.xA, self.yA = 0, 0
        self.xB, self.yB = 0, initialY
        self.xC, self.yC = 0, 0
        # These three points have different growing parameters randomly defined
        self.dxA = 5
        self.dxC = random.randint(0, 12)
        self.dyB = random.choice([0.5, 0.7, 1])

    def move(self):
        self.xA += self.dxA
        middle = (self.xC - self.xA) //2
        self.xB = self.xA + middle
        self.yB += self.dyB
        self.dxC += 3
        self.xC = self.xA + self.dxC

    def draw(self, canvas):
        if (self.side == 'right'):
            xA, yA = self.app.width//2 + self.xA, self.app.height//2
            xB, yB = self.app.width//2 + self.xB, self.app.height//2 - self.yB
            xC, yC = self.app.width//2 + self.xC, self.app.height//2
        else:
            xA, yA = self.app.width//2 - self.xA, self.app.height//2
            xB, yB = self.app.width//2 - self.xB, self.app.height//2 - self.yB
            xC, yC = self.app.width//2 - self.xC, self.app.height//2
        canvas.create_polygon(xA, yA, xB, yB, xC, yC, fill = self.app.groundC)

class Player(Game):
    def __init__(self, app):
        self.app = app
        # The player position is predefined in positions that match the same
        # positions of the objects in game 
        self.pos = 0
        self.y = self.app.height - 100
        # Player sprites animation
        image = app.loadImage('player_sprites.png')
        imageS = app.loadImage('player_sprites_blue.png')
        # Player running
        spritesNo = 6
        coordinates = (0, 0, 100, 170)
        self.sprites = Game.getSprites(image, spritesNo, coordinates)
        self.spritesS = Game.getSprites(imageS, spritesNo, coordinates)
        # Player jumping
        spritesNo = 2
        coordinatesJump = (600, 0, 700, 170)
        self.jump = Game.getSprites(image, spritesNo, coordinatesJump)
        self.jumpS = Game.getSprites(imageS, spritesNo, coordinatesJump)
        self.currentSpr = 0
    
    def move(self, dpos):
        if (self.app.gameOver == False):
            self.pos += dpos
            if self.pos < 0: self.pos = 0
            elif self.pos > 3: self.pos = 3

    def draw(self, canvas):
        dx = self.app.width//4
        x = (dx - dx//2) + (self.pos * dx)
        y = self.y
        # Sprites depending on mode and action (running or jumping)
        if (self.app.specialMode == True):
            sprites = self.spritesS
            if (self.app.jumping == True):
                sprites = self.jumpS
        else:
            sprites = self.sprites
            if (self.app.jumping == True):
                sprites = self.jump
        sprite = sprites[self.currentSpr]
        canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite))
        
class Objects(Game):
    def __init__(self, app):
        # A list of all the objects displayed in the game. I have decided to 
        # use a list in order to keep track of the order of placement of the
        # objects in the screen to draw them correctly after.
        self.lst = []
        self.app = app
    
    def move(self):
        remove = 0
        for obj in self.lst:
            obj.move()
            if isinstance(obj, Coin) or isinstance(obj, Win95):
                spritesNo = len(obj.sprites)
                obj.currentSpr = (1 + obj.currentSpr) % spritesNo
            # When an object reach the canvas limit it is removed
            if (obj.y > 130):
                remove += 1
        for _ in range(remove):
            self.lst.pop(0)

    def draw(self, canvas):
        if (len(self.lst) != 0):
            for i in range(len(self.lst)-1, -1, -1):
                self.lst[i].draw(canvas)

class Head(Objects):
    def __init__(self, app, pos):
        self.app = app
        self.pos = pos
        self.size = 1
        self.x, self.y = 0, 1
        self.dy = 0
        self.app.objects.lst.append(self)
        # Object sprites animation
        image = app.loadImage('head_sprites.png')
        spritesNo = 5
        coordinates = (0, 0, 230, 365)
        self.sprites = Game.getSprites(image, spritesNo, coordinates)
        self.sprite = self.sprites[self.pos]
        self.broken = self.sprites[4]

    def move(self):
        # Speed of the object movement
        self.dy += 0.15
        self.y += self.dy
        # Perspective traslation equation for each head path
        if   (self.pos == 0): self.x = -3 * self.y
        elif (self.pos == 1): self.x = -self.y
        elif (self.pos == 2): self.x = +self.y
        elif (self.pos == 3): self.x = +3 * self.y
        # Perspective size transformation for each head
        self.size = self.y

    def draw(self, canvas):
        x, y = self.app.width//2 + self.x, self.app.height//2 + self.y
        image = self.sprite
        s = self.size
        imageW, imageH = int(2.30 * s), int(3.65 * s)
        image = image.resize((imageW, imageH), Image.NEAREST)
        canvas.create_image(x, y, image = ImageTk.PhotoImage(image))

class Coin(Objects):
    def __init__(self, app, pos):
        self.app = app
        self.pos = pos
        self.size = 1
        self.x, self.y = 0, 1
        self.dy = 0
        self.app.objects.lst.append(self)
        # Object sprites animation
        image = app.loadImage('coin_sprites.png')
        spritesNo = 6
        coordinates = (0, 0, 80, 80)
        self.sprites = Game.getSprites(image, spritesNo, coordinates)
        self.currentSpr = 0
        self.catch = False

    def move(self):
        if (self.catch == False):
            # Speed of the movement of the coin
            self.dy += 0.2
            self.y += self.dy
            # Perspective traslation equation for each coin path
            if   (self.pos == 0): self.x = -(4/3)  * self.y
            elif (self.pos == 1): self.x = -(0.45) * self.y
            elif (self.pos == 2): self.x = +(0.45) * self.y
            elif (self.pos == 3): self.x = +(4/3)  * self.y
            # Perspective size transformation for each coin
            self.size = self.y
        else:
            self.x = self.x
            self.y -= 50
            self.size = 80

    def draw(self, canvas):
        x, y = self.app.width//2 + self.x, self.app.height//2 + self.y
        image = self.sprites[self.currentSpr]
        s = self.size
        imageW, imageH = int(0.8 * s), int(0.8 * s)
        if (imageW == 0) or (imageH == 0): imageW, imageH = 1, 1
        image = image.resize((imageW, imageH), Image.NEAREST)
        canvas.create_image(x, y, image = ImageTk.PhotoImage(image))

class Win95(Objects):
    def __init__(self, app, pos):
        self.app = app
        self.pos = pos
        self.size = 1
        self.x, self.y = 0, 1
        self.dy = 0
        self.app.objects.lst.append(self)
        # Object sprites animation
        image = app.loadImage('win95_sprites.png')
        spritesNo = 6
        coordinates = (0, 0, 80, 80)
        self.sprites = Game.getSprites(image, spritesNo, coordinates)
        self.currentSpr = 0

    def move(self):
        # Speed of the movement of the Win95 logo
        self.dy += 0.2
        self.y += self.dy
        # Perspective traslation equation for each Win95 logo path
        if   (self.pos == 0): self.x = -(4/3)  * self.y
        elif (self.pos == 1): self.x = -(0.45) * self.y
        elif (self.pos == 2): self.x = +(0.45) * self.y
        elif (self.pos == 3): self.x = +(4/3)  * self.y
        # Perspective size transformation for each Win95 logo
        self.size = self.y

    def draw(self, canvas):
        x, y = self.app.width//2 + self.x, self.app.height//2 + self.y
        image = self.sprites[self.currentSpr]
        s = self.size
        imageW, imageH = int(0.8 * s), int(0.8 * s)
        if (imageW == 0) or (imageH == 0): imageW, imageH = 1, 1
        image = image.resize((imageW, imageH), Image.NEAREST)
        canvas.create_image(x, y, image = ImageTk.PhotoImage(image))

Vaporscape(width = 800, height = 600)