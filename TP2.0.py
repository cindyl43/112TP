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
# TP2 check
# Adpated from my Tetris hw
# Using cmu 112 animation framework
# Imported cmu_112_graphics
#################################################

def appStarted (app):
    app.level = 1
    app.rows = app.level + 2
    app.cols = app.level + 2
    app.margin, app.topMargin, = gameDimensions()
    app.score = 0
    app.tips = 0
    app.solutions = []
    resetLevel(app)
    app.leastStep = 0

def resetLevel(app):
    app.controlRow = 0
    app.controlCol = 0
    app.cellSize = (app.width - 2*app.margin) / app.rows
    app.emptyColor = "white"
    app.board = [([app.emptyColor] * app.cols) for row in range(app.rows)]
    app.heartList = [([False] * app.cols) for row in range(app.rows)]
    app.heartDirs = [([0] * app.cols) for row in range(app.rows)]
    #app.leastStep = leastPossibleTurns(app)
    app.state = "play"
    app.userMove = [[0,0,0]]
    app.steps = 0
    generateHeartsBoard(app)

def raiseLevel(app):
    app.level += 1
    app.rows += 1
    app.cols += 1
    app.margin, app.topMargin, = gameDimensions()
    resetLevel(app)
    app.state = "play"

def leastPossibleTurns(app):
    #app.leastStep = 
    #backTrack steps
    pass

def keyPressed(app, event):
    # Move control to the heart that it is interacting with  
    if (event.key == "Down"):
        if app.state == "play":
            moveControl(app, +1, 0)
    elif (event.key == "Left"):
        if app.state == "play":
            moveControl(app, 0, -1)
    elif (event.key == "Right"):
        if app.state == "play":
            moveControl(app, 0, +1) 
    elif (event.key == "Up"):
        if app.state == "play":
            moveControl(app, -1, 0)
    # Press Return to turn
    elif (event.key == "Enter"): 
        if app.state == "play":
            rotateHearts(app)
            app.userMove.extend ([[app.controlRow,app.controlCol,1]])
            allHeartsUp(app)
            app.steps += 1
        elif app.state == "win":
            raiseLevel (app)
        elif app.state == "start":
            app.state = "play"
    # Giving 1 tip when there is one
    elif (event.key == "t"):
        if app.state == "play":
            if app.tips <= 0:
                app.state = "paused"
            else:
                app.tips -= 1
        elif app.state == "paused":
            app.state = "play"    
    # Reset level
    elif (event.key == "r"):
        resetLevel (app) 
    # Undo one step 
    elif (event.key == "z"):
        if app.state == "play":
            if len(app.userMove) > 1:
                retrieveStep (app)
            else:
                app.state = "start"   

'''
def controlSolver (col, heartRow):
# Recursive backtracker to place control
    if col == app.cols:
    # base case: when col are both the last one
        return # some kind of soulution (2dlist of where the possible controls)]
    else:
        for row in range(app.rows):
            if controlIsLegal (row, col, controlRow):
                # app.controlPosition on this spot
                solution = controlSolver (col+1, heartRow)
                if (solution != None): # if it works
                    return solution
                # if it didn't work
                controlRow[col] -= 1 # pick up the control
        return None
'''

def rotateHearts(app):
    row = app.controlRow
    col = app.controlCol
    #rotate up heart
    upRow, upCol = row-1, col
    turnHeart (app, upRow, upCol)
    #rotate left heart
    leftRow, leftCol = row, col-1
    turnHeart (app, leftRow, leftCol)
    #rotate down heart 
    downRow, downCol = row+1, col
    turnHeart (app, downRow, downCol)
    #rotate right heart
    rightRow, rightCol = row, col+1
    turnHeart (app, rightRow, rightCol)
    return 

def turnHeart (app, row, col):
    if (-1 < row < app.rows) and (-1 < col < app.cols):
        if app.heartList [row][col] == True:
            if app.heartDirs[row][col] == 3:
                app.heartDirs[row][col] = 0
            elif app.heartDirs[row][col] < 3:
                app.heartDirs[row][col] += 1
        else:
            app.heartList [row][col] = 0

def moveControl (app, drow, dcol):
    app.controlRow += drow
    app.controlCol += dcol
    if (not controlIsLegal(app)):
        app.controlRow -= drow
        app.controlCol -= dcol
        return False
    app.userMove.extend([[app.controlRow, app.controlCol, 0]])
    return True

def controlIsLegal(app):
    # Checks whether the piece is on board
    if (app.controlRow < 0
        or app.controlRow >= app.rows
        or app.controlCol < 0
        or app.controlCol >= app.cols):
        return False
    return True

def retrieveStep (app):
    currentMove = app.userMove.pop()
    turn = currentMove [2] #whether it turned
    if turn == 1:
        fourBackTurn (app, app.controlRow, app.controlCol)
        app.steps -= 1
    else:
        row = app.userMove[-1][0]
        col = app.userMove[-1][1]
        app.controlRow = row
        app.controlCol = col
    
def allHeartsUp(app):
    #check that all hearts face up
    for row in range (len(app.heartList)):
        for col in range (len(app.heartList[0])):
            if app.heartList [row][col] == True:
                if app.heartDirs[row][col] != 0:
                    return False
    app.state = "win"
    return True

# randomly generated board
def RandomSolvableBoard(app):
    numHearts = 0
    # range of number of hearts in the given level
    totalHearts = random.randint (int(0.6 * app.rows * app.cols), \
        int(0.8 * app.rows * app.cols))
    while numHearts < totalHearts:
        heartRow = random.randint (0, app.rows-1)
        heartCol = random.randint (0, app.cols-1)
        if app.heartList [heartRow][heartCol] == False:
            app.heartList [heartRow][heartCol] = True
            numHearts += 1
        if app.heartList [heartRow][heartCol] == True:
            fourBackTurn (app, heartRow, heartCol)
    return 

def fourBackTurn (app, row, col):
    #rotate up heart
    upRow, upCol = row-1, col
    counterHeart (app, upRow, upCol)
    #rotate left heart
    leftRow, leftCol = row, col-1
    counterHeart (app, leftRow, leftCol)
    #rotate down heart 
    downRow, downCol = row+1, col
    counterHeart (app, downRow, downCol)
    #rotate right heart
    rightRow, rightCol = row, col+1
    counterHeart (app, rightRow, rightCol)

def counterHeart (app, row, col):
    if ((-1 < row < app.rows) and (-1 < col < app.cols)):
        if app.heartDirs[row][col] == 0:
            app.heartDirs[row][col] = 3
        elif app.heartDirs[row][col] >0:
            app.heartDirs[row][col] -= 1

def generateHeartsBoard(app):
    RandomSolvableBoard(app)
    
def drawBoard(app, canvas, rows, cols):
    for row in range(rows):
        for col in range(cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def drawCell(app, canvas, row, col, color):
    x0 = app.margin + col*app.cellSize
    x1 = x0 + app.cellSize
    y0 = app.topMargin + row*app.cellSize
    y1 = y0 + app.cellSize
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=3)

def drawScore(app, canvas):
    textMargin = app.topMargin // 2
    canvas.create_text(app.width/5, textMargin,
    text = f'Moves: {app.steps}/ {app.leastStep}',
    fill = "black", 
    font = "Arial 18 bold")

def drawTip(app, canvas):
    textMargin = app.topMargin // 2
    canvas.create_text(5*app.width/6, textMargin,
    text = f'Tips: {app.tips}',
    fill = "black", 
    font = "Arial 18 bold")

def drawHearts(app, canvas):
    for row in range(len(app.heartList)):
        for col in range(len(app.heartList[0])):
            if app.heartList[row][col] == True:
                rotate = app.heartDirs[row][col]
                drawSingleHeart(app, canvas, row, col, rotate)


def drawSingleHeart(app, canvas, row, col, dirs):
    x0 = app.margin + col * app.cellSize
    y0 = app.topMargin + row * app.cellSize
    image = Image.open('heart.png')
    heart = image.resize((int(app.cellSize), int(app.cellSize)))
    rot_0 = heart
    rot_1 = heart.rotate (270)
    rot_2 = heart.rotate (180)
    rot_3 = heart.rotate (90)
    if dirs == 0:
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(rot_0), anchor=NW)
    elif dirs == 1:
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(rot_1), anchor=NW)
    elif dirs == 2:
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(rot_2), anchor=NW)
    elif dirs == 3:
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(rot_3), anchor=NW)

def drawControl(app, canvas):
    x0 = app.margin + app.controlCol * app.cellSize
    y0 = app.topMargin + app.controlRow * app.cellSize
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

def drawPassed (app, canvas):
    if app.state == "win":
        canvas.create_rectangle(0, app.height //3,
                                app.width, 2 * app.height //3,
                                fill = "light green", width=0 )
        canvas.create_text(app.width//2, app.height //2.3,
                            text = 'Congrats!',
                            fill = "black",
                            font = "Arial 22 bold")
        canvas.create_text(app.width//2, app.height //1.95,
                            text = f'Press ENTER to level {app.level+1}',
                            fill = "black",
                            font = "Arial 22 bold")                   
        canvas.create_text(app.width//2, app.height //1.7,
                        text = "Press R to replay",
                        fill = "black",
                        font = "Arial 22 bold")

def drawStarted (app, canvas):
    #draw page game starts
    canvas.create_rectangle(0, app.height //3,
                                app.width, 2 * app.height //3,
                                fill = "light green", width=0 )
    canvas.create_text(app.width//2, app.height //2.3,
                        text = "Press ENTER to resume",
                        fill = "black",
                        font = "Arial 22 bold")
    canvas.create_text(app.width//2, app.height //1.8,
                        text = "Press R to restart with a new map",
                        fill = "black",
                        font = "Arial 22 bold")

def redrawAll(app, canvas):
    #background color
    canvas.create_rectangle(0, 0, app.width, app.height, fill="light blue") 
    drawBoard(app, canvas, app.rows, app.cols)
    drawHearts(app, canvas)
    drawScore(app, canvas)
    drawTip(app, canvas)
    drawControl(app, canvas)
    drawPassed (app, canvas)
    if app.state == "paused":
        drawPaused (app, canvas)
    if app.state == "start":
        drawStarted (app, canvas)

def playHearts():
    margin, topMargin = gameDimensions()
    runApp(width= 400 , height= 450)

def gameDimensions():
    margin = 10
    topMargin = 50
    return (margin, topMargin)

#################################################
# main
#################################################

def main():
    cs112_f20_linter.lint()
    playHearts()

if __name__ == '__main__':
    main()
