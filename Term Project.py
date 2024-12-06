from cmu_graphics import *
import math
import random
from PIL import Image
import time

def onAppStart(app):
    app.width = 600
    app.height = 800
    app.backgroundPic = CMUImage(Image.open('background.jpg'))
    app.court = CMUImage(Image.open('court.webp'))
    app.gameStart = False
    courtLine = Image.open('line.png')
    app.courtLine = CMUImage(courtLine.crop((150, 103, 725, 121)))
    
    app.highScore = loadHighScore()

    app.userX = 300
    app.userY = 600
    app.userSpeed = 0
    app.userVelocityX = 0
    app.userVelocityY = 0
    app.targetX = app.userX
    app.targetY = app.userY

    app.aiX = 300
    app.aiY = 200
    app.aiSpeed = 10
    app.aiMovementSpeed = 0 
    app.aiTargetX = app.aiX

    app.aiLeftX = 150
    app.aiLeftY = 200
    app.aiTargetLeftx = 225 
    app.aiTargetLefty = 150 
    app.aiTargetRightx = 375  
    app.aiTargetRighty = 150


    app.aiRightX = 450
    app.aiRightY = 200
    
    app.gameOver = CMUImage(Image.open('gameOver.jpg'))

    app.puckX = 300
    app.puckY = 400
    app.puckRadius = 25
    app.puckVelocityX = 4
    app.puckVelocityY = 3

    app.userScore = 0
    app.aiScore = 0

    app.counter = 3
    app.pause = False

    app.goalWidth = 200
    app.goalHeight = 20

    app.stepsPerSecond = 200

    app.gameEnd = False

    app.start = False

    app.easySelected='mediumseagreen'
    app.medSelected='orange'
    app.hardSelected='firebrick'

    app.classic = False
    app.squareMode = False
    app.twoPlayer = False

    app.classicFill = None
    app.squareFill = None
    app.twoPlayerFill = None

    app.borderWidth = 2
    app.increasing = True

    app.reactionDelay = 0
#Amazon Q{
def loadHighScore():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        saveHighScore(0)
        return 0

def saveHighScore(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))
# } Amazon Q

def redrawAll(app):
    if not app.gameStart:
        drawImage(app.backgroundPic, 0, 0, width=600, height=800)
        drawLabel(f'High Score = {str(app.highScore)}', 450, 30, size=40, font='Britannic Bold', fill='white')
        drawLabel("Air Hockey", 300, 200, font='Snap ITC', size=60, fill='white')
        drawLabel('Choose Difficulty', 300, 415, font='Trebuchet MS', size=32, fill='white')
        drawLabel('Easy', 150, 490, size=35, font='Stencil', fill=app.easySelected)
        drawLabel('Medium', 300, 490, size=35, font='Stencil', fill=app.medSelected)
        drawLabel('Hard', 450, 490, size=35, font='Stencil', fill=app.hardSelected)
        drawLabel('Choose Mode', 300, 615, size=30, font='Trebuchet MS', fill='white')
        drawLabel('Classic', 300, 700, size=30, font='Bauhaus 93', fill='dodgerblue')
        drawRect(225, 665, 150, 75, fill=app.classicFill, border='dodgerblue', opacity=30)
        drawLabel('Square Mode', 125, 700, size=20, font='Bauhaus 93', fill='peachpuff')
        drawRect(50, 665, 150, 75, fill=app.squareFill, border='peachpuff', opacity=30)
        drawLabel('1 vs 2', 475, 700, size=30, font='Bauhaus 93', fill='magenta')
        drawRect(400, 665, 150, 75, fill=app.twoPlayerFill, border='magenta', opacity=30)
    elif app.gameEnd:
        drawImage(app.gameOver, 0, 0, width = app.width, height=app.height)
    else:   
        drawImage(app.court, 0, 0, width=600, height=800)
        drawImage(app.courtLine, 0, 0, width = 200, height=10)
        drawImage(app.courtLine, 400, 0, width = 200, height=10)
        drawImage(app.courtLine, 0, 790, width = 200, height=10)
        drawImage(app.courtLine, 400, 790, width = 200, height=10)
        drawImage(app.courtLine, 0, 395, width = 600, height=10)
        drawLabel(str(app.userScore), 550, 440, size=50, fill='white')
        drawLabel(str(app.aiScore), 550, 360, size=50, fill='white')
        drawCircle(app.puckX, app.puckY, 25, fill=None, border='red', borderWidth=5)
        
        if app.classic:
            drawCircle(app.userX, app.userY, 50, fill='blue')
            drawCircle(app.userX, app.userY, 25, fill='blue', border='black')
            drawCircle(app.aiX, app.aiY, 50, fill='green')
            drawCircle(app.aiX, app.aiY, 25, fill='green', border='black')
            
        if app.squareMode:
            drawRect(app.userX, app.userY, 100, 100, fill='blue', align='center')
            drawRect(app.aiX, app.aiY, 100, 100, fill='green', align='center')

        if app.twoPlayer:
            drawCircle(app.userX, app.userY, 50, fill='blue')
            drawCircle(app.userX, app.userY, 25, fill='blue', border='black')
            drawCircle(app.aiLeftX, app.aiLeftY, 50, fill='green')
            drawCircle(app.aiLeftX, app.aiLeftY, 25, fill='green', border='black') 
            drawCircle(app.aiRightX, app.aiRightY, 50, fill='green')
            drawCircle(app.aiRightX, app.aiRightY, 25, fill='green', border='black') 
        
        if app.pause:
            drawLabel('SCORE!!!', 300, 200, size=80, font='Cooper Black', fill='white')
            drawLabel(f'Game resumes in {str(app.counter)}', 300, 375, font='Courier', size=50, fill='white')
        if app.start:
            drawLabel(f'Game starts in {str(app.counter)}', 300, 375, font='Courier', size=50, fill='white')

def onMousePress(app, mouseX, mouseY):
    if not app.gameStart:
        if (125 <= mouseX <= 175) & (480 <= mouseY <= 500):
            app.easySelected = 'white'
            app.medSelected = 'orange'
            app.hardSelected = 'firebrick'
            app.aiSpeed = 1.75
            app.aiMovementSpeed = 1
            app.reactionDelay = 0.5
        if (275 <= mouseX <= 325) & (480 <= mouseY <= 500):
            app.easySelected = 'mediumseagreen'
            app.medSelected = 'white'
            app.hardSelected = 'firebrick'
            app.aiSpeed = 2.1
            app.aiMovementSpeed = 1.15
            app.reactionDelay = 0.6
        if (425 <= mouseX <= 475) & (480 <= mouseY <= 500):
            app.easySelected = 'mediumseagreen'
            app.medSelected = 'orange'
            app.hardSelected = 'white'
            app.aiSpeed = 2.35
            app.aiMovementSpeed = 1.4
            app.reactionDelay = 0.7
        if (app.easySelected == 'white' or app.medSelected == 'white' or app.hardSelected == 'white') and (225 <= mouseX <= 375) and (665<= mouseY <= 740):
            app.gameStart = True
            app.classic = True
            startGame(app)
        if (app.easySelected == 'white' or app.medSelected == 'white' or app.hardSelected == 'white') and (50 <= mouseX <= 200) and (665<= mouseY <= 740):
            app.gameStart = True
            app.squareMode = True
            startGame(app)
        if (app.easySelected == 'white' or app.medSelected == 'white' or app.hardSelected == 'white') and (400 <= mouseX <= 550) and (665<= mouseY <= 740):
            app.gameStart = True
            app.twoPlayer = True
            startGame(app)
        
    if app.gameEnd and (205 <= mouseX <= 255) and (200 <= mouseY <= 225):
        app.gameStart = False
        app.gameEnd = False
        app.easySelected = 'mediumseagreen'
        app.medSelected = 'orange'
        app.hardSelected = 'firebrick'
        app.twoPlayer = False
        app.classic = False
        app.squareMode = False
        app.width = 600
        app.height = 800
        startGame(app)
    elif app.gameEnd and (265 <= mouseX <= 305) and (200 <= mouseY <= 225): 
        exit()
        
def onMouseMove(app, mouseX, mouseY):
    if not app.gameStart:
        if (400 <= mouseX <= 550) and (665<= mouseY <= 740):
            app.twoPlayerFill = 'white'
            app.squareFill = None
            app.classicFill = None
        elif (50 <= mouseX <= 200) and (665<= mouseY <= 740):
            app.squareFill = 'white'
            app.twoPlayerFill = None
            app.classicFill = None
        elif (225 <= mouseX <= 375) and (665<= mouseY <= 740):
            app.classicFill = 'white'
            app.twoPlayerFill = None
            app.squareFill = None
        else:
            app.twoPlayerFill = None
            app.squareFill = None
            app.classicFill = None

    else:
        app.targetX = max(60, min(540, mouseX))
        app.targetY = max(400 + 50, min(740, mouseY))

def onStep(app):
    if app.pause:
        app.counter -= 1
        if app.counter == 0:
            app.pause = False
            app.stepsPerSecond = 200
            app.counter = 3
    
    if app.start:
        app.counter -= 1
        if app.counter == 0:
            app.start = False
            app.stepsPerSecond = 200
            app.counter = 3

    if not app.start and not app.pause:

        if app.classic or app.squareMode:
            moveAIPaddle(app)
            checkAICollision(app)
        else:
            moveLeftAI(app)
            moveRightAI(app)
            checkLeftAICollision(app)
            checkRightAICollision(app)

        #Amazon Q{
        dx = app.targetX - app.userX
        dy = app.targetY - app.userY
        app.userSpeed = math.sqrt(dx**2 + dy**2) * 0.2
        app.userX += dx * 0.5
        app.userY += dy * 0.5
    
        app.puckX += app.puckVelocityX
        app.puckY += app.puckVelocityY

        if app.classic or app.twoPlayer:
            dx = app.puckX - app.userX
            dy = app.puckY - app.userY
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance <= 75:
                if distance == 0:
                    distance = 0.0001
                

                normalX = dx / distance
                normalY = dy / distance
              
                currentSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
                bounciness = 3  
            #} Amazon Q    
                if ((app.puckVelocityX != 0 and app.puckVelocityY != 0) or \
                (app.puckVelocityX == 0 and app.puckVelocityY != 0) or \
                (app.puckVelocityX != 0 and app.puckVelocityY == 0)) \
                and (app.userSpeed < 5.5):
                    
                    bounciness *= 0.15
                else: 
                    bounciness *= 2.5

                if currentSpeed < 0.1:  
                    bounciness = 2.5 
                    hitSpeed = max(app.userSpeed * 15, 5)
                    app.puckVelocityX = normalX * hitSpeed
                    app.puckVelocityY = normalY * hitSpeed
                else:
                    app.puckVelocityX = normalX * currentSpeed * bounciness
                    app.puckVelocityY = normalY * currentSpeed * bounciness
        
                #Amazon Q {
                overlap = 75 - distance
                app.puckX += normalX * overlap
                app.puckY += normalY * overlap
                # } Amazon Q
        else:
            strikerSize = 100  
            halfSize = strikerSize / 2  
            puckSize = 50

            userLeft = app.userX - halfSize
            userRight = app.userX + halfSize
            userTop = app.userY - halfSize
            userBottom = app.userY + halfSize

            puckLeft = app.puckX - puckSize/2
            puck_right = app.puckX + puckSize/2
            puckTop = app.puckY - puckSize/2
            puckBottom = app.puckY + puckSize/2

            if (userLeft < puck_right and userRight > puckLeft and
                userTop < puckBottom and userBottom > puckTop):
                
                dx = app.puckX - app.userX
                dy = app.puckY - app.userY
                magnitude = math.sqrt(dx**2 + dy**2)
                
                currentSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
                bounciness = 3  
                # }Amazon Q

                if ((app.puckVelocityX != 0 and app.puckVelocityY != 0) or \
                (app.puckVelocityX == 0 and app.puckVelocityY != 0) or \
                (app.puckVelocityX != 0 and app.puckVelocityY == 0)) \
                and (app.userSpeed < 5.5):
                    
                    bounciness *= 0.15
                else: 
                    bounciness *= 2.5

                if currentSpeed < 0.1:  
                    bounciness = 2.5  
                    hitSpeed = max(app.userSpeed * 10, 3)  
                    app.puckVelocityX = (dx/magnitude) * hitSpeed
                    app.puckVelocityY = (dy/magnitude) * hitSpeed   
                else:
                    app.puckVelocityX = (dx / magnitude) * currentSpeed * bounciness
                    app.puckVelocityY = (dy / magnitude) * currentSpeed * bounciness
                
                #Amazon Q { 
                if abs(dx) > abs(dy):
                    collisionNormalX = 1 if dx > 0 else -1
                    collisionNormalY = 0
                else:
                    collisionNormalX = 0
                    collisionNormalY = 1 if dy > 0 else -1

                overlap = strikerSize/2 + puckSize/2 - magnitude
                if overlap > 0:
                    app.puckX += collisionNormalX * overlap
                    app.puckY += collisionNormalY * overlap
                # } Amazon Q

        if app.puckX - app.puckRadius <= 0:  
            app.puckX = app.puckRadius  # Amazon Q
            app.puckVelocityX *= -1 

        if app.puckX + app.puckRadius >= app.width:  
            app.puckX = app.width - app.puckRadius  # Amazon Q
            app.puckVelocityX *= -1 

        if app.puckY - app.puckRadius <= 0:  
            app.puckY = app.puckRadius  # Amazon Q
            app.puckVelocityY *= -1 

        if app.puckY + app.puckRadius >= app.height:  
            app.puckY = app.height - app.puckRadius  # Amazon Q
            app.puckVelocityY *= -1  

        if (225 <= app.puckX <= 375) and (app.puckY <= 30):  
            app.userScore += 1
            if app.userScore > app.highScore:
                app.highScore = app.userScore
                saveHighScore(app.highScore)
            resetPuck(app)

        if (225 <= app.puckX <= 375) and (app.puckY >= 770):  
            app.aiScore += 1
            if app.aiScore == 3:
                app.gameEnd = True
                app.width = 520
                app.height = 360
            else:
                resetPuck(app)

        app.puckVelocityX *= 0.98
        app.puckVelocityY *= 0.98

        # Amazon Q {
        maxSpeed = 35
        puckSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
        if puckSpeed > maxSpeed:
            scalingFactor = maxSpeed / puckSpeed
            app.puckVelocityX *= scalingFactor
            app.puckVelocityY *= scalingFactor
        # } Amazon Q

def resetPuck(app):
    app.puckX = 300
    app.puckY = 400
    app.aiX = 300
    app.aiY = 200
    app.aiLeftX = 150
    app.aiLeftY = 200
    app.aiRightX = 450
    app.aiRightY = 200
    app.puckVelocityX = 0
    app.puckVelocityY = 0
    app.userX = 300
    app.userY = 600
    app.pause = True
    app.stepsPerSecond = 1

def startGame(app):
    app.puckX = 300
    app.puckY = 400
    app.puckVelocityX = 0
    app.puckVelocityY = 0
    app.userX = 300
    app.userY = 600
    app.aiLeftX = 100
    app.aiLeftY = 200
    app.aiRightX = 500
    app.aiRightY = 200
    app.aiX = 300
    app.aiY = 200
    app.start = True
    app.userScore = 0
    app.aiScore = 0
    app.stepsPerSecond = 1


def moveAIPaddle(app):
    aiSpeed = 6 
    predictionTime = 0.75  
    defaultX = 300
    defaultY = 150

    if app.puckY <= app.height / 2: 
        predictedPuckX = app.puckX + app.puckVelocityX * predictionTime
        predictedPuckY = app.puckY + app.puckVelocityY * predictionTime
        
        
        if predictedPuckY < 0:
            timeToWall = -app.puckY / app.puckVelocityY if app.puckVelocityY < 0 else 0
            postBouncePuckX = app.puckX + app.puckVelocityX * timeToWall
            postBouncePuckY = 0 + abs(app.puckVelocityY) * (predictionTime - timeToWall)
            
            if postBouncePuckX < 0:
                postBouncePuckX = -postBouncePuckX
            elif postBouncePuckX > 600:
                postBouncePuckX = 600 - (postBouncePuckX - 600)
            
            app.aiTargetX = postBouncePuckX
            app.aiTargetY = postBouncePuckY - 50  
        else:
            predictedPuckX = max(0, min(600, predictedPuckX))
            predictedPuckY = max(0, predictedPuckY)
            app.aiTargetX = predictedPuckX
            app.aiTargetY = predictedPuckY - 50  
            
    else:
        centerDeadzone = 75
        if abs(app.aiX - defaultX) > centerDeadzone:
            app.aiTargetX = defaultX
        else:
            app.aiTargetX = app.aiX  
            
        if abs(app.aiY - defaultY) > 5:
            app.aiTargetY = defaultY
        else:
            app.aiTargetY = app.aiY

    distanceToTarget = math.sqrt((app.aiTargetX - app.aiX)**2 + 
                                 (app.aiTargetY - app.aiY)**2)
    

    if distanceToTarget > 100:
        aiSpeed =  8 
    elif distanceToTarget > 50:
        aiSpeed = 7
    else:
        aiSpeed = 6  
    
    aiSpeed *= app.aiMovementSpeed
    
    moveX = app.aiTargetX - app.aiX
    moveY = app.aiTargetY - app.aiY
    
    distance = math.sqrt(moveX**2 + moveY**2)
    if distance > 0:
        app.aiX += (moveX / distance) * aiSpeed
        app.aiY += (moveY / distance) * aiSpeed

    app.aiX = max(0, min(600, app.aiX))
    app.aiY = max(0, min(350, app.aiY))  

def onKeyPress(app, key):
    if key == 'q':
        app.gameStart = False
        app.classic = False
        app.squareMode = False
        app.twoPlayer = False

#Amazon Q{
def checkAICollision(app):
    if app.classic:
        dx = app.puckX - app.aiX
        dy = app.puckY - app.aiY
        speed = math.sqrt(dx**2 + dy**2) * 0.2
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= 75:
            if distance == 0:
                distance = 0.0001

            normalX = dx / distance
            normalY = dy / distance

            currentSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)

            bounciness = 0.9
            if ((app.puckVelocityX != 0 and app.puckVelocityY != 0) or \
            (app.puckVelocityX == 0 and app.puckVelocityY != 0) or \
            (app.puckVelocityX != 0 and app.puckVelocity == 0)) \
            and (speed < 5.5):     
                bounciness *= 0.15
            else: 
                bounciness *= app.aiSpeed

            if currentSpeed < 0.1:  
                app.aiSpeed = 1.5 
                hitSpeed = max(app.userSpeed * 15, 5)  
                app.puckVelocityX = normalX * hitSpeed
                app.puckVelocityY = normalY * hitSpeed
            else:
                app.puckVelocityX = normalX * currentSpeed * bounciness
                app.puckVelocityY = normalY * currentSpeed * bounciness

            overlap = 75 - distance
            app.puckX += normalX * overlap
            app.puckY += normalY * overlap
    elif app.squareMode:
        strikerSize = 100  
        halfSize = strikerSize / 2  
        puckSize = 50

        userLeft = app.aiX - halfSize
        userRight = app.aiX + halfSize
        userTop = app.aiY - halfSize
        userBottom = app.aiY + halfSize

        puckLeft = app.puckX - puckSize/2
        puck_right = app.puckX + puckSize/2
        puckTop = app.puckY - puckSize/2
        puckBottom = app.puckY + puckSize/2

        if (userLeft < puck_right and userRight > puckLeft and
            userTop < puckBottom and userBottom > puckTop):
            
            dx = app.puckX - app.aiX
            dy = app.puckY - app.aiY
            speed = math.sqrt(dx**2 + dy**2) * 0.2
            magnitude = math.sqrt(dx**2 + dy**2)
            
            currentSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
            bounciness = 0.9  
            
            if ((app.puckVelocityX != 0 and app.puckVelocityY != 0) or \
            (app.puckVelocityX == 0 and app.puckVelocityY != 0) or \
            (app.puckVelocityX != 0 and app.puckVelocityY == 0)) \
            and (speed < 5.5):
                
                bounciness *= 0.15
            else: 
                bounciness *= app.aiSpeed

            if currentSpeed < 0.1:  
                bounciness = 2.5  
                hitSpeed = max(app.userSpeed * 10, 3)  
                app.puckVelocityX = (dx/magnitude) * hitSpeed
                app.puckVelocityY = (dy/magnitude) * hitSpeed   
            else:
                app.puckVelocityX = (dx / magnitude) * currentSpeed * bounciness
                app.puckVelocityY = (dy / magnitude) * currentSpeed * bounciness

            if abs(dx) > abs(dy):
                collisionNormalX = 1 if dx > 0 else -1
                collisionNormalY = 0
            else:
                collisionNormalX = 0
                collisionNormalY = 1 if dy > 0 else -1

            overlap = strikerSize/2 + puckSize/2 - magnitude
            if overlap > 0:
                app.puckX += collisionNormalX * overlap
                app.puckY += collisionNormalY * overlap
# } Amazon Q

#same as moveAIPaddle(app)
def moveLeftAI(app):
    aiSpeed = 6  
    predictionTime = 0.75 
    defaultX = 150
    defaultY = 150
    if app.puckY <= app.height / 2: 
        predictedPuckX = app.puckX + app.puckVelocityX * predictionTime
        predictedPuckY = app.puckY + app.puckVelocityY * predictionTime
        if predictedPuckX < 300:
            if predictedPuckY < 0:
                timeToWall = -app.puckY / app.puckVelocityY if app.puckVelocityY < 0 else 0
 
                postBouncePuckX = app.puckX + app.puckVelocityX * timeToWall
                postBouncePuckY = 0 + abs(app.puckVelocityY) * (predictionTime - timeToWall)

                if postBouncePuckX < 0:
                    postBouncePuckX = -postBouncePuckX
                elif postBouncePuckX > 600:
                    postBouncePuckX = 600 - (postBouncePuckX - 600)

                app.aiTargetLeftx = postBouncePuckX
                app.aiTargetLefty = postBouncePuckY - 50  
            else:
                predictedPuckX = max(0, min(600, predictedPuckX))
                predictedPuckY = max(0, predictedPuckY)
                app.aiTargetLeftx = predictedPuckX
                app.aiTargetLefty = predictedPuckY - 50  
            
    else:
        deadzone = 10 

        if abs(app.aiLeftX - defaultX) > deadzone:
            app.aiTargetLeftx = defaultX
        else:
            app.aiTargetLeftx = app.aiLeftX 
            
        if abs(app.aiLeftY - defaultY) > deadzone:
            app.aiTargetLefty = defaultY
        else:
            app.aiTargetLefty = app.aiLeftY

    distanceToTarget = math.sqrt((app.aiTargetLeftx - app.aiLeftX)**2 + 
                                 (app.aiTargetLefty - app.aiLeftY)**2)
    
    if distanceToTarget > 100:
        aiSpeed = 8  
    elif distanceToTarget > 50:
        aiSpeed = 7
    else:
        aiSpeed = 6  
    
    aiSpeed *= app.aiMovementSpeed

    moveX = app.aiTargetLeftx - app.aiLeftX
    moveY = app.aiTargetLefty - app.aiLeftY

    distance = math.sqrt(moveX**2 + moveY**2)
    if distance > 0:
        app.aiLeftX += (moveX / distance) * aiSpeed
        app.aiLeftY += (moveY / distance) * aiSpeed

    app.aiLeftX = max(0, min(600, app.aiLeftX))
    app.aiLeftY = max(0, min(350, app.aiLeftY)) 

#same as moveAIPaddle(app)
def moveRightAI(app):
    aiSpeed = 6  
    predictionTime = 0.75 
    defaultX = 450
    defaultY = 150
    if app.puckY <= 400:
        predictedPuckX = app.puckX + app.puckVelocityX * predictionTime
        predictedPuckY = app.puckY + app.puckVelocityY * predictionTime
        if predictedPuckX >= 300:
            if predictedPuckY < 0:
                timeToWall = -app.puckY / app.puckVelocityY if app.puckVelocityY < 0 else 0

                postBouncePuckX = app.puckX + app.puckVelocityX * timeToWall
                postBouncePuckY = 0 + abs(app.puckVelocityY) * (predictionTime - timeToWall)

                if postBouncePuckX < 0:
                    postBouncePuckX = -postBouncePuckX
                elif postBouncePuckX > 600:
                    postBouncePuckX = 600 - (postBouncePuckX - 600)
                
                app.aiTargetRightx = postBouncePuckX
                app.aiTargetRighty = postBouncePuckY - 50 
            else:
                predictedPuckX = max(0, min(600, predictedPuckX))
                predictedPuckY = max(0, predictedPuckY)
                app.aiTargetRightx = predictedPuckX
                app.aiTargetRighty = predictedPuckY - 50  
            
    else:
        deadzone = 10 

        if abs(app.aiRightX - defaultX) > deadzone:
            app.aiTargetRightx = defaultX
        else:
            app.aiTargetRightx = app.aiRightX 
            
        if abs(app.aiRightY - defaultY) > deadzone:
            app.aiTargetRighty = defaultY
        else:
            app.aiTargetRighty = app.aiRightY 

    distanceToTarget = math.sqrt((app.aiTargetRightx - app.aiRightX)**2 + 
                                 (app.aiTargetRighty - app.aiRightY)**2)
    
    if distanceToTarget > 100:
        aiSpeed = 8 
    elif distanceToTarget > 50:
        aiSpeed = 7
    else:
        aiSpeed = 6
    
    aiSpeed *= app.aiMovementSpeed

    moveX = app.aiTargetRightx - app.aiRightX
    moveY = app.aiTargetRighty - app.aiRightY

    distance = math.sqrt(moveX**2 + moveY**2)
    if distance > 0:
        app.aiRightX += (moveX / distance) * aiSpeed
        app.aiRightY += (moveY / distance) * aiSpeed

    app.aiRightX = max(0, min(600, app.aiRightX))
    app.aiRightY = max(0, min(350, app.aiRightY)) 

#same as checkAICollision(app)
def checkLeftAICollision(app):
    dx = app.puckX - app.aiLeftX
    dy = app.puckY - app.aiLeftY
    speed = math.sqrt(dx**2 + dy**2) * 0.2
    distance = math.sqrt(dx**2 + dy**2)

    if distance <= 75:
        if distance == 0:
            distance = 0.0001
        
        normalX = dx / distance
        normalY = dy / distance
        
        currentSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
        
        bounciness = 0.9
        if ((app.puckVelocityX != 0 and app.puckVelocityY != 0) or \
        (app.puckVelocityX == 0 and app.puckVelocityY != 0) or \
        (app.puckVelocityX != 0 and app.puckVelocity == 0)) \
        and (speed < 5.5):     
            bounciness *= 0.15
        else: 
            bounciness *= app.aiSpeed

        if currentSpeed < 0.1:
            app.aiSpeed = 2.5  
            hitSpeed = max(app.userSpeed * 15, 5)
            app.puckVelocityX = normalX * hitSpeed
            app.puckVelocityY = normalY * hitSpeed
        else:
            app.puckVelocityX = normalX * currentSpeed * bounciness
            app.puckVelocityY = normalY * currentSpeed * bounciness

        overlap = 75 - distance
        app.puckX += normalX * overlap
        app.puckY += normalY * overlap

#same as checkAICollision(app)
def checkRightAICollision(app):
    dx = app.puckX - app.aiRightX
    dy = app.puckY - app.aiRightY
    speed = math.sqrt(dx**2 + dy**2) * 0.2
    distance = math.sqrt(dx**2 + dy**2)
    
    
    if distance <= 75:
        if distance == 0:
            distance = 0.0001
        
        normalX = dx / distance
        normalY = dy / distance
        
        currentSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
        
        bounciness = 0.9
        if ((app.puckVelocityX != 0 and app.puckVelocityY != 0) or \
        (app.puckVelocityX == 0 and app.puckVelocityY != 0) or \
        (app.puckVelocityX != 0 and app.puckVelocity == 0)) \
        and (speed < 5.5):     
            bounciness *= 0.15
        else: 
            bounciness *= app.aiSpeed

        if currentSpeed < 0.1: 
            app.aiSpeed = 2.5  
            hitSpeed = max(app.userSpeed * 15, 5)
            app.puckVelocityX = normalX * hitSpeed
            app.puckVelocityY = normalY * hitSpeed
        else:
            app.puckVelocityX = normalX * currentSpeed * bounciness
            app.puckVelocityY = normalY * currentSpeed * bounciness

        overlap = 75 - distance
        app.puckX += normalX * overlap
        app.puckY += normalY * overlap

def main():
    runApp()

main()