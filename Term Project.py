from cmu_graphics import *
import math
import random
from PIL import Image
import time

def onAppStart(app):
    app.width = 600
    app.height = 800
    app.backgroundPic = CMUImage(Image.open('background.jpg'))
    puck = Image.open('court.webp')
    app.court = CMUImage(puck.crop((220, 100, 820, 900)))
    app.gameStart = False

    app.userX = 300
    app.userY = 600
    app.userSpeed = 0
    app.targetX = app.userX
    app.targetY = app.userY

    app.aiX = 300
    app.aiY = 200
    app.aiSpeed = 10
    app.aiMovementSpeed = 0 
    app.aiTargetX = app.aiX 
    app.aiLeftX = 150
    app.aiLeftY = 200

    app.aiRightX = 450
    app.aiRightY = 200

    app.puckX = 300
    app.puckY = 400
    app.puckRadius = 25
    app.puckVelocityX = 0
    app.puckVelocityY = 0
    # app.userPuck = Image.open('userPuck.png', 300, 400)

    app.userScore = 0
    app.aiScore = 0

    app.counter = 3
    app.pause = False

    app.goalWidth = 200
    app.goalHeight = 20

    app.stepsPerSecond = 200

    app.gameEnd = False

    app.start = False

    app.easySelected=False
    app.medSelected=False
    app.hardSelected=False

    app.lastHitTime = time.time()

    app.classic = False
    app.squareMode = False
    app.twoPlayer = False

    app.classicFill = None
    app.squareFill = None
    app.twoPlayerFill = None

    app.borderWidth = 2
    app.increasing = True

def redrawAll(app):
    if not app.gameStart:
        drawImage(app.backgroundPic, 0, 0, width=600, height=800)
        drawLabel("Air Hockey", 300, 200, font='Snap ITC', size=60, fill='white')
        drawLabel('Choose Difficulty', 300, 415, font='Trebuchet MS', size=32, fill='white')
        drawLabel('Easy', 150, 490, size=35, font='Stencil', fill='mediumseagreen', bold=app.easySelected)
        drawLabel('Medium', 300, 490, size=35, font='Stencil', fill='orange', bold=app.medSelected)
        drawLabel('Hard', 450, 490, size=35, font='Stencil', fill='firebrick', bold=app.hardSelected)
        drawLabel('Choose Mode', 300, 615, size=30, font='Trebuchet MS', fill='white')
        drawLabel('Classic', 300, 700, size=30, font='Bauhaus 93', fill='dodgerblue')
        drawRect(225, 665, 150, 75, fill=app.classicFill, border='dodgerblue', opacity=30)
        drawLabel('Square Mode', 125, 700, size=20, font='Bauhaus 93', fill='peachpuff')
        drawRect(50, 665, 150, 75, fill=app.squareFill, border='peachpuff', opacity=30)
        drawLabel('1 vs 2', 475, 700, size=30, font='Bauhaus 93', fill='magenta')
        drawRect(400, 665, 150, 75, fill=app.twoPlayerFill, border='magenta', opacity=30)
    elif app.gameEnd:
        if app.userScore > app.aiScore:
            drawLabel('You Won!', 300, 200, size=40)
        else:
            drawLabel('You Lost', 300, 200, size=40)
        drawLabel('Play Again', 300, 450, size=20)
        drawRect(225, 415, 150, 75, fill=None, border='black')
    else:
        
        drawImage(app.court, 0, 0, width=600, height=800)
        drawLabel(str(app.userScore), 550, 440, size=50, fill='white')
        drawLabel(str(app.aiScore), 550, 360, size=50, fill='white')
        drawPulsingBorder(app)
        
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
            drawLabel('SCORE!!!', 300, 200, size=80, fill='white')
            drawLabel(f'Game resumes in {str(app.counter)}', 300, 400, size=50, fill='white')
        if app.start:
            drawLabel(f'Game starts in {str(app.counter)}', 300, 400, size=50, fill='white')


def drawPulsingBorder(app):
    # Outer glow
    drawCircle(app.puckX, app.puckY, app.puckRadius + 4, 
              fill=None, border='red', 
              borderWidth=app.borderWidth)
    # Main circle
    drawCircle(app.puckX, app.puckY,  app.puckRadius, 
              fill=None, border='red', borderWidth=3)


def onMousePress(app, mouseX, mouseY):
    if not app.gameStart:
        if (125 <= mouseX <= 175) & (480 <= mouseY <= 500):
            app.easySelected = True
            app.medSelected = False
            app.hardSelected = False
            app.aiSpeed = 4
            app.aiMovementSpeed = 4
        if (275 <= mouseX <= 325) & (480 <= mouseY <= 500):
            app.easySelected = False
            app.medSelected = True
            app.hardSelected = False
            app.aiSpeed = 7
            app.aiMovementSpeed = 5
        if (425 <= mouseX <= 475) & (480 <= mouseY <= 500):
            app.easySelected = False
            app.medSelected = False
            app.hardSelected = True
            app.aiSpeed = 10
            app.aiMovementSpeed = 6
        if (app.easySelected or app.medSelected or app.hardSelected) and (225 <= mouseX <= 375) and (665<= mouseY <= 740):
            app.gameStart = True
            app.classic = True
            startGame(app)
        if (app.easySelected or app.medSelected or app.hardSelected) and (50 <= mouseX <= 200) and (665<= mouseY <= 740):
            app.gameStart = True
            app.squareMode = True
            startGame(app)
        if (app.easySelected or app.medSelected or app.hardSelected) and (400 <= mouseX <= 550) and (665<= mouseY <= 740):
            app.gameStart = True
            app.twoPlayer = True
            startGame(app)
        
    if app.gameEnd and (225 <= mouseX <= 375) and (415 <= mouseY <= 490):
        app.gameStart = False
        app.gameEnd = False
        startGame(app)
        
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
            

    if app.gameStart and not app.pause and not app.start:
        if app.increasing:
            app.borderWidth += 0.2
            if app.borderWidth >= 8:
                app.increasing = False
        else:
            app.borderWidth -= 0.2
            if app.borderWidth <= 2:
                app.increasing = True
        # Update user paddle position
        dx = app.targetX - app.userX
        dy = app.targetY - app.userY
        app.userSpeed = math.sqrt(dx**2 + dy**2) * 0.2
        app.userX += dx * 0.5
        app.userY += dy * 0.5

        if app.classic or app.squareMode:
            moveAIPaddle(app)
            checkAICollision(app)
        else:
            moveLeftAI(app)
            moveRightAI(app)
            checkLeftAICollision(app)
            checkRightAICollision(app)
        # if ((app.puckY - app.puckRadius <= 10) or (app.puckX - app.puckRadius <= 10) 
        #     or (app.puckX + app.puckRadius >= app.width - 10)):
        #     wait(app)
        # Update puck position
        app.puckX += app.puckVelocityX
        app.puckY += app.puckVelocityY
        
        # Check collision between paddle and puck
        if app.classic or app.twoPlayer:
            distance = math.sqrt((app.userX - app.puckX)**2 + (app.userY - app.puckY)**2)
            if distance < 75:
                dx = app.puckX - app.userX
                dy = app.puckY - app.userY
                magnitude = math.sqrt(dx**2 + dy**2)
                if magnitude != 0:
                    app.puckVelocityX = (dx / magnitude) * app.userSpeed * 3 
                    app.puckVelocityY = (dy / magnitude) * app.userSpeed * 3
        elif app.squareMode:
            strikerSize = 100  # Changed to 100
            halfSize = strikerSize / 2  # Now 50
            puckSize = 50

            # User striker bounds
            userLeft = app.userX - halfSize
            userRight = app.userX + halfSize
            userTop = app.userY - halfSize
            userBottom = app.userY + halfSize

            # Puck bounds
            puckLeft = app.puckX - puckSize/2
            puck_right = app.puckX + puckSize/2
            puckTop = app.puckY - puckSize/2
            puckBottom = app.puckY + puckSize/2

            if (userLeft < puck_right and userRight > puckLeft and
                userTop < puckBottom and userBottom > puckTop):
                
                dx = app.puckX - app.userX
                dy = app.puckY - app.userY
                magnitude = math.sqrt(dx**2 + dy**2)
                
                if magnitude != 0:
                    app.puckVelocityX = (dx / magnitude) * app.userSpeed * 3
                    app.puckVelocityY = (dy / magnitude) * app.userSpeed * 3

                # Prevent sticking
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
        
        # Handle puck collisions with walls
        if app.puckX - app.puckRadius <= 0:  # Left wall
            app.puckX = app.puckRadius  # Prevent overlap
            app.puckVelocityX *= -1  # Reverse X velocity

        if app.puckX + app.puckRadius >= app.width:  # Right wall
            app.puckX = app.width - app.puckRadius  # Prevent overlap
            app.puckVelocityX *= -1  # Reverse X velocity

        if app.puckY - app.puckRadius <= 0:  # Top wall
            app.puckY = app.puckRadius  # Prevent overlap
            app.puckVelocityY *= -1  # Reverse Y velocity

        if app.puckY + app.puckRadius >= app.height:  # Bottom wall
            app.puckY = app.height - app.puckRadius  # Prevent overlap
            app.puckVelocityY *= -1  # Reverse Y velocity

        if (225 <= app.puckX <= 375) and (app.puckY <= 30):  # Top goal
            app.userScore += 1
            if app.userScore == 5:
                app.gameEnd = True
            else:
                resetPuck(app)

        if (225 <= app.puckX <= 375) and (app.puckY >= 770):  # Bottom goal
            app.aiScore += 1
            if app.aiScore == 5:
                app.gameEnd = True
            else:
                resetPuck(app)

        app.puckVelocityX *= 0.98
        app.puckVelocityY *= 0.98

        maxSpeed = 40
        puckSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
        if puckSpeed > maxSpeed:
            scalingFactor = maxSpeed / puckSpeed
            app.puckVelocityX *= scalingFactor
            app.puckVelocityY *= scalingFactor

def resetPuck(app):
    app.puckX = 300
    app.puckY = 400
    app.aiX = 300
    app.aiY = 200
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
    app.start = True
    app.stepsPerSecond = 1

import math

def moveAIPaddle(app):
    aiSpeed = 6  
    predictionTime = 0.75  # Predict for 0.75 seconds

    if app.puckY <= app.height / 2:  # React only when the puck is on AI's side
        # Calculate predicted X and Y positions in 0.75 seconds
        predictedPuckX = app.puckX + app.puckVelocityX * predictionTime
        predictedPuckY = app.puckY + app.puckVelocityY * predictionTime

        # Predict if puck will hit the top wall (Y = 0)
        if predictedPuckY < 0:
            # Time to hit the wall
            timeToWall = -app.puckY / app.puckVelocityY if app.puckVelocityY < 0 else 0
            
            # Predict position after hitting the wall
            postBouncePuckX = app.puckX + app.puckVelocityX * timeToWall
            postBouncePuckY = 0 + abs(app.puckVelocityY) * (predictionTime - timeToWall)
            
            # Clamp X to bounds (walls at X=0 and X=600)
            if postBouncePuckX < 0:
                postBouncePuckX = -postBouncePuckX
            elif postBouncePuckX > 600:
                postBouncePuckX = 600 - (postBouncePuckX - 600)
            
            # AI intercepts after the bounce
            app.aiTargetX = postBouncePuckX
            app.aiTargetY = postBouncePuckY - 50  # Move above the bounce point to intercept from top
        else:
            # Normal prediction
            predictedPuckX = max(0, min(600, predictedPuckX))
            predictedPuckY = max(0, predictedPuckY)
            app.aiTargetX = predictedPuckX
            app.aiTargetY = predictedPuckY - 50  # Stay slightly above the puck
            
    else:
        # Return to defensive position if the puck is not on AI's side
        app.aiTargetX = app.width / 2
        app.aiTargetY = 150

    # Increase movement speed based on distance to target
    distanceToTarget = math.sqrt((app.aiTargetX - app.aiX)**2 + 
                                 (app.aiTargetY - app.aiY)**2)
    
    # Boost speed for large distances
    if distanceToTarget > 100:
        aiSpeed = 5
    
    # Move AI paddle towards target
    if app.aiX < app.aiTargetX:
        app.aiX += min(aiSpeed, app.aiTargetX - app.aiX)
    elif app.aiX > app.aiTargetX:
        app.aiX -= min(aiSpeed, app.aiX - app.aiTargetX)

    if app.aiY < app.aiTargetY:
        app.aiY += min(aiSpeed, app.aiTargetY - app.aiY)
    elif app.aiY > app.aiTargetY:
        app.aiY -= min(aiSpeed, app.aiY - app.aiTargetY)

    # Keep AI within bounds
    app.aiX = max(0, min(600, app.aiX))
    app.aiY = max(0, min(350, app.aiY))  # Assuming bottom bound for AI is Y=350




#Amazon Q{
def checkAICollision(app):
    if app.classic:
        distance = math.sqrt((app.aiX - app.puckX)**2 + (app.aiY - app.puckY)**2)
        if distance < 75:
            collisionNormalX = (app.puckX - app.aiX) / distance
            collisionNormalY = (app.puckY - app.aiY) / distance
            dx = app.puckX - app.aiX
            dy = app.puckY - app.aiY
            magnitude = math.sqrt(dx**2 + dy**2)
            if magnitude != 0:
                app.puckVelocityX = (dx / magnitude) * app.aiSpeed * 3 
                app.puckVelocityY = (dy / magnitude) * app.aiSpeed * 3

        # Offset puck slightly to prevent overlap after collision
            overlap = 75 - distance
            app.puckX += collisionNormalX * overlap * 0.5
            app.puckY += collisionNormalY * overlap * 0.5
    elif app.squareMode:
        strikerSize = 100  # Changed to 100
        halfSize = strikerSize / 2  # Now 50
        puckSize = 50

        # AI striker bounds
        aiLeft = app.aiX - halfSize
        aiRight = app.aiX + halfSize
        aiTop = app.aiY - halfSize
        aiBottom = app.aiY + halfSize

        # Puck bounds
        puckLeft = app.puckX - puckSize/2
        puckRight = app.puckX + puckSize/2
        puckTop = app.puckY - puckSize/2
        puckBottom = app.puckY + puckSize/2

        if (aiLeft < puckRight and aiRight > puckLeft and
            aiTop < puckBottom and aiBottom > puckTop):
            
            dx = app.puckX - app.aiX
            dy = app.puckY - app.aiY
            
            # Determine which side of the square was hit
            if abs(dx) > abs(dy):
                collisionNormalX = 1 if dx > 0 else -1
                collisionNormalY = 0
            else:
                collisionNormalX = 0
                collisionNormalY = 1 if dy > 0 else -1

            magnitude = math.sqrt(dx**2 + dy**2)
            if magnitude != 0:
                app.puckVelocityX = (dx / magnitude) * app.aiSpeed * 3
                app.puckVelocityY = (dy / magnitude) * app.aiSpeed * 3

            # Prevent sticking
            overlap = strikerSize/2 + puckSize/2 - magnitude
            if overlap > 0:
                app.puckX += collisionNormalX * overlap
                app.puckY += collisionNormalY * overlap

def moveLeftAI(app):
    aiSpeed = 6  
    predictionTime = 0.75 
    if app.puckY <= app.height / 2:
        
        predictedPuckX = app.puckX + app.puckVelocityX * predictionTime
        predictedPuckY = app.puckY + app.puckVelocityY * predictionTime
        if predictedPuckX < 300:
        # Predict if puck will hit the top wall (Y = 0)
            if predictedPuckY < 0:
                # Time to hit the wall
                timeToWall = -app.puckY / app.puckVelocityY if app.puckVelocityY < 0 else 0
                
                # Predict position after hitting the wall
                postBouncePuckX = app.puckX + app.puckVelocityX * timeToWall
                postBouncePuckY = 0 + abs(app.puckVelocityY) * (predictionTime - timeToWall)
                
                # Clamp X to bounds (walls at X=0 and X=600)
                if postBouncePuckX < 0:
                    postBouncePuckX = -postBouncePuckX
                elif postBouncePuckX > 600:
                    postBouncePuckX = 600 - (postBouncePuckX - 600)
                
                # AI intercepts after the bounce
                app.aiTargetLeftX = postBouncePuckX
                app.aiTargetLeftY = postBouncePuckY - 50  # Move above the bounce point to intercept from top
            else:
                # Normal prediction
                predictedPuckX = max(0, min(600, predictedPuckX))
                predictedPuckY = max(0, predictedPuckY)
                app.aiTargetLeftX = predictedPuckX
                app.aiTargetLeftY = predictedPuckY - 50  # Stay slightly above the puck
                
        else:
            # Return to defensive position if the puck is not on AI's side
            app.aiTargetLeftX = 150
            app.aiTargetLeftY = 150

        # Increase movement speed based on distance to target
        distanceToTarget = math.sqrt((app.aiTargetLeftX - app.aiLeftX)**2 + 
                                    (app.aiTargetLeftY - app.aiLeftY)**2)
        
        # Boost speed for large distances
        if distanceToTarget > 100:
            aiSpeed = 5
        
        # Move AI paddle towards target
        if app.aiLeftX < app.aiTargetLeftX:
            app.aiLeftX += min(aiSpeed, app.aiTargetLeftX - app.aiLeftX)
        elif app.aiLeftX > app.aiTargetLeftX:
            app.aiLeftX -= min(aiSpeed, app.aiLeftX - app.aiTargetLeftX)

        if app.aiLeftY < app.aiTargetLeftY:
            app.aiLeftY += min(aiSpeed, app.aiTargetLeftY - app.aiLeftY)
        elif app.aiLeftY > app.aiTargetLeftY:
            app.aiLeftY -= min(aiSpeed, app.aiLeftY - app.aiTargetLeftY)

        # Keep AI within bounds
        app.aiLeftX = max(0, min(600, app.aiLeftX))
        app.aiLeftY = max(0, min(350, app.aiLeftY))

def moveRightAI(app):
    aiSpeed = 6  
    predictionTime = 0.75 
    if app.puckY <= app.height / 2:
        
        predictedPuckX = app.puckX + app.puckVelocityX * predictionTime
        predictedPuckY = app.puckY + app.puckVelocityY * predictionTime
        if predictedPuckX >= 300:
        # Predict if puck will hit the top wall (Y = 0)
            if predictedPuckY < 0:
                # Time to hit the wall
                timeToWall = -app.puckY / app.puckVelocityY if app.puckVelocityY < 0 else 0
                
                # Predict position after hitting the wall
                postBouncePuckX = app.puckX + app.puckVelocityX * timeToWall
                postBouncePuckY = 0 + abs(app.puckVelocityY) * (predictionTime - timeToWall)
                
                # Clamp X to bounds (walls at X=0 and X=600)
                if postBouncePuckX < 0:
                    postBouncePuckX = -postBouncePuckX
                elif postBouncePuckX > 600:
                    postBouncePuckX = 600 - (postBouncePuckX - 600)
                
                # AI intercepts after the bounce
                app.aiTargetRightX = postBouncePuckX
                app.aiTargetRightY = postBouncePuckY - 50  # Move above the bounce point to intercept from top
            else:
                # Normal prediction
                predictedPuckX = max(0, min(600, predictedPuckX))
                predictedPuckY = max(0, predictedPuckY)
                app.aiTargetRightX = predictedPuckX
                app.aiTargetRightY = predictedPuckY - 50  # Stay slightly above the puck
                
        else:
            # Return to defensive position if the puck is not on AI's side
            app.aiTargetRightX = 450
            app.aiTargetRightY = 150

        # Increase movement speed based on distance to target
        distanceToTarget = math.sqrt((app.aiTargetRightX - app.aiRightX)**2 + 
                                    (app.aiTargetRightY - app.aiRightY)**2)
        
        # Boost speed for large distances
        if distanceToTarget > 100:
            aiSpeed = 5
        
        # Move AI paddle towards target
        if app.aiRightX < app.aiTargetRightX:
            app.aiRightX += min(aiSpeed, app.aiTargetRightX - app.aiRightX)
        elif app.aiRightX > app.aiTargetRightX:
            app.aiRightX -= min(aiSpeed, app.aiRightX - app.aiTargetRightX)

        if app.aiRightY < app.aiTargetRightY:
            app.aiRightY += min(aiSpeed, app.aiTargetRightY - app.aiRightY)
        elif app.aiRightY > app.aiTargetRightY:
            app.aiRightY -= min(aiSpeed, app.aiRightY - app.aiTargetRightY)

        # Keep AI within bounds
        app.aiRightX = max(0, min(600, app.aiRightX))
        app.aiRightY = max(0, min(350, app.aiRightY))

def checkLeftAICollision(app):
    strikerSize = 100
    halfSize = strikerSize / 2
    puckSize = 50

    # Left AI striker bounds
    aiLeft = app.aiLeftX - halfSize
    aiRight = app.aiLeftX + halfSize
    aiTop = app.aiLeftY - halfSize
    aiBottom = app.aiLeftY + halfSize

    # Puck bounds
    puckLeft = app.puckX - puckSize/2
    puckRight = app.puckX + puckSize/2
    puckTop = app.puckY - puckSize/2
    puckBottom = app.puckY + puckSize/2

    if (aiLeft < puckRight and aiRight > puckLeft and
        aiTop < puckBottom and aiBottom > puckTop):
        
        dx = app.puckX - app.aiLeftX
        dy = app.puckY - app.aiLeftY
        
        if abs(dx) > abs(dy):
            collisionNormalX = 1 if dx > 0 else -1
            collisionNormalY = 0
        else:
            collisionNormalX = 0
            collisionNormalY = 1 if dy > 0 else -1

        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude != 0:
            app.puckVelocityX = (dx / magnitude) * app.aiSpeed * 3
            app.puckVelocityY = (dy / magnitude) * app.aiSpeed * 3

        overlap = strikerSize/2 + puckSize/2 - magnitude
        if overlap > 0:
            app.puckX += collisionNormalX * overlap
            app.puckY += collisionNormalY * overlap

def checkRightAICollision(app):
    strikerSize = 100
    halfSize = strikerSize / 2
    puckSize = 50

    # Right AI striker bounds
    aiLeft = app.aiRightX - halfSize
    aiRight = app.aiRightX + halfSize
    aiTop = app.aiRightY - halfSize
    aiBottom = app.aiRightY + halfSize

    # Puck bounds
    puckLeft = app.puckX - puckSize/2
    puckRight = app.puckX + puckSize/2
    puckTop = app.puckY - puckSize/2
    puckBottom = app.puckY + puckSize/2

    if (aiLeft < puckRight and aiRight > puckLeft and
        aiTop < puckBottom and aiBottom > puckTop):
        
        dx = app.puckX - app.aiRightX
        dy = app.puckY - app.aiRightY
        
        if abs(dx) > abs(dy):
            collisionNormalX = 1 if dx > 0 else -1
            collisionNormalY = 0
        else:
            collisionNormalX = 0
            collisionNormalY = 1 if dy > 0 else -1

        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude != 0:
            app.puckVelocityX = (dx / magnitude) * app.aiSpeed * 3
            app.puckVelocityY = (dy / magnitude) * app.aiSpeed * 3

        overlap = strikerSize/2 + puckSize/2 - magnitude
        if overlap > 0:
            app.puckX += collisionNormalX * overlap
            app.puckY += collisionNormalY * overlap

def main():
    runApp()

main()