import cs112_f20_linter
import os, math, copy, random
from PIL import Image
from time import sleep

from cmu_112_graphics import *

#################################################
# Helper functions
# Cited from hw7 15112 Fall 2020
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# TP1 check
# Adpated from my Tetris hw
# Using cmu 112 animation framework
# Imported cmu_112_graphics
#################################################

def appStarted (app):
    app.rows, app.cols, app.margin, \
        app.topMargin, app.cellSize = gameDimensions()
    app.emptyColor = "white"
    app.board = [([app.emptyColor] * app.cols) for row in range(app.rows)]
    app.score = 0
    app.tips = 0
    app.paused = False
    app.control = 1
    app.controlPosition = [0, 0]
    app.win = False
    app.controlRow = 0
    app.controlCol = 0
    app.solutions = []
    app.moves = []
    app.level = 1
    app.heartList = [([False] * app.cols) for row in range(app.rows)]
    app.heartDirs =[]
    #levelStarted(app)
    app.gameOver = False
    app.level = 1
    app.tip = 0

def keyPressed(app, event):
    if controlIsLegal (app):
        # Move control to the heart that it is interacting with  
        if (event.key == "Down"):
            moveControl(app, +1, 0)
        elif (event.key == "Left"):
            moveControl(app, 0, -1)
        elif (event.key == "Right"):
            moveControl(app, 0, +1)    
        elif (event.key == "Up"):
            moveControl(app, -1, 0)   
    # Giving 1 tip
    elif (event.key == "t"):
        if app.tips > 0:
            app.tips -= 1
        else:
            app.paused = True
    # Reset game
    elif (event.key == "r"):
        appStarted(app) #for the level?  
    # Rotate hearts
    elif (event.key == "return"):
        rotateHearts(app, drow, dcol)

def rotateHearts(app, drow, dcol):
    pass

def selectHeart(app, drow, dcol):
    pass

def moveControl (app, drow, dcol):
    app.controlRow += drow
    app.controlCol += dcol
    if (not controlIsLegal(app)):
        app.controlRow -= drow
        app.controlCol -= dcol
        return False
    return True

def controlIsLegal(app):
    # Checks whether the piece is on board
    if (app.controlRow < 0
        or app.controlRow >= app.rows + 1
        or app.controlCol < 0
        or app.controlCol >= app.cols + 1):
        return False
    
def timerFired(app):
    # check if wins, move to the next level
    #if AllHeartsUp (app)== True:
        #generateLevel (app)
    pass

def allHeartsUp(app):
    #check that all hearts face up
    for direction in app.heartDirs:
        if direction != (0,0):
            return False
    return True

def generateLevel(app):
    app.level += 1
    app.rows += 1
    app.cols += 1

def generateHeartsSolution(app):
    numHearts = 0
    # range of number of hearts in the given level
    totalHearts = random.randit (int(0.6 * app.rows * app.cols), \
        int(0.8 * app.rows * app.cols))
    while numHearts < totalHearts:
        heartRow = random.randit (0, app.rows)
        heartCol = random.randit (0, app.cols)
        if app.heartList [heartRow][heartCol] == False:
            app.heartList [heartRow][heartCol] = True
            numHearts += 1
        
def drawCell(app, canvas, row, col, color):
    x0 = app.margin + col*app.cellSize
    x1 = x0 + app.cellSize
    y0 = app.topMargin + row*app.cellSize
    y1 = y0 + app.cellSize
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=3)

def drawBoard(app, canvas, rows, cols):
    for row in range(rows):
        for col in range(cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def drawScore(app, canvas):
    textMargin = app.topMargin // 2
    canvas.create_text(app.width/6, textMargin,
    text = f'Score: {app.score}',
    fill = "black", 
    font = "Arial 18 bold")

def drawTip(app, canvas):
    textMargin = app.topMargin // 2
    canvas.create_text(5*app.width/6, textMargin,
    text = f'Tips: {app.tip}',
    fill = "black", 
    font = "Arial 18 bold")
'''
def drawHearts(app, canvas):
    for row in range(len(app.heartList)):
        for col in range(len(app.heartList[0])):
            if app.heartList[row][col] == True:
                x0 = col * app.cellSize
                y0 = row * app.cellSize
                heart = Image.open('heart.png')
                canvas.create_image(x0, y0, image=ImageTk.PhotoImage(heart), \
                    anchor=NW)
'''
def drawSingleHeart(app, canvas):
    x0 = app.margin
    y0 = app.topMargin
    image = Image.open('heart.png')
    heart = image.resize((int(app.cellSize), int(app.cellSize)))
    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(heart), anchor=NW)

def drawControl(app, canvas):
    x0 = app.margin + app.controlRow
    y0 = app.topMargin + app.controlCol
    gear = Image.open('control.png')
    control = gear.resize((int(app.cellSize), int(app.cellSize)))
    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(control), anchor=NW)

def drawPaused(app, canvas):
    #draw page for any errors occured
    canvas.create_rectangle(app.margin, app.height //3,
                            app.width-app.margin, 2 * app.height //3,
                            fill = "black")
    canvas.create_text(app.width//2, app.height //2,
                        text = "No More Tips",
                        fill = "yellow",
                        font = "Arial 22 bold")

def redrawAll(app, canvas):
    #background color
    canvas.create_rectangle(0, 0, app.width, app.height, fill="light blue") 
    drawBoard(app, canvas, app.rows, app.cols)
    drawHearts(app, canvas)
    drawScore(app, canvas)
    drawTip(app, canvas)
    drawControl(app, canvas)
    if app.paused == True:
        time = time.time()
        if time <= 3:
            drawPaused (app, canvas)

        
def playHearts():
    rows, cols, margin, topMargin, cellSize = gameDimensions()
    runApp(width= 400 , height= 450)

def gameDimensions():
    # Returns the dimensions of the board
    # Players can change the default values according to their preference
    rows = 3
    cols = 3
    margin = 10
    topMargin = 50
    cellSize = (400 - 2*margin) / rows
    return (rows, cols, margin, topMargin, cellSize)

#################################################
# main
#################################################

def main():
    cs112_f20_linter.lint()
    playHearts()

if __name__ == '__main__':
    main()
