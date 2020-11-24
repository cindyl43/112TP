import cs112_f20_linter
import os, math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
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
# TP0 demo
#################################################

#class Board (object):

def appStarted (app):
        app.score = 0
        app.tip = 0
        app.paused = False
        app.control = [0,0]
        app.playerMoves = []
        app.playerMoveCount = 0

def keyPressed(app, event):
     # Move control to the heart that it is interacting with  
    if (event.key == "Down"):
        moveFallingPiece(app, +1, 0)
    elif (event.key == "Left"):
        moveFallingPiece(app, 0, -1)
    elif (event.key == "Right"):
        moveFallingPiece(app, 0, +1)    
    elif (event.key == "Up"):
        rotateFallingPiece(app)    
    # Giving 1 tip
    elif (event.key == "t"):
        if app.tips > 0:
            app.tips -= 1
        app.paused = True
    # Reset game
    elif (event.key == "r"):
        appStarted(app) #for the level?  
    # Rotate hearts
    elif (event.key == "return"):
        rotateHearts(app, drow, dcol)

def importImages(app, data):
    app.controlImage = PhotoImage(file="control.png")
    app.heartImage = PhotoImage(file="heart.png")
    app.brickImage = PhotoImage(file="brick.png")

def rotateHearts(app, drow, dcol):

def selectHeart(app, drow, dcol):



def timerFired(app):


def drawHearts(app, canvas):

def drawBoard(app, canvas, rows, cols):
    for row in range(rows):
        for col in range(cols):
            drawCell(app, canvas, row, col, app.board[row][col])


def drawScore(app, canvas):
    textMargin = 0.5*app.margin
    canvas.create_text(app.width/2, textMargin,
    text = f'Score: {app.score}',
    fill = "medium blue", 
    font = "Arial 18 bold")

def drawPlayer(app, canvas):
    canvas.create_image(m+data.board.playerPosition[1]*s, m+data.board.playerPosition[0]*s,
        image=data.playerImage, anchor=NW)

def 

def drawPaused(app, canvas)
#draw page for any errors occured

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="orange")
    drawBoard(app, canvas)
    drawHearts(app, canvas)
    drawScore(app, canvas)
    if app.paused = True:
        drawPaused (app, canvas)

def playHearts():
    runApp(width=width, height=height)

#################################################
# main
#################################################

def main():
    cs112_f20_linter.lint()
    playHearts()

if __name__ == '__main__':
    main()


