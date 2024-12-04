from cmu_graphics import *
import math
import random
from PIL import Image
import time

def onAppStart(app):
    app.width = 600
    app.height = 800
    app.gameStart = False

    app.userX = 300
    app.userY = 600
    app.userSpeed = 0
    app.targetX = app.userX
    app.targetY = app.userY
    app.userTurn = True

    app.aiX = 300
    app.aiY = 200
    app.aiSpeed = 10
    app.aiMovementSpeed = 0 
    app.aiTargetX = app.aiX 

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

def redrawAll(app):
    if not app.gameStart:
        drawLabel("Single Player Air Hockey", 300, 200, size=40)
        drawLabel('Easy', 100, 500, size=40, bold=app.easySelected)
        drawLabel('Medium', 300, 500, size=40, bold=app.medSelected)
        drawLabel('Hard', 500, 500, size=40, bold=app.hardSelected)
        drawLabel('Classic', 300, 635, size=30)
        drawRect(225, 600, 150, 75, fill=None, border='black')
        drawLabel('Square Mode', 125, 635, size=20)
        drawRect(50, 600, 150, 75, fill=None, border='black')
        drawLabel('1 vs 2', 475, 635, size=30)
        drawRect(400, 600, 150, 75, fill=None, border='black')
    elif app.gameEnd:
        if app.userScore > app.aiScore:
            drawLabel('You Won!', 300, 200, size=40)
        else:
            drawLabel('You Lost', 300, 200, size=40)
        drawLabel('Play Again', 300, 450, size=20)
        drawRect(225, 415, 150, 75, fill=None, border='black')
    else:
        # if app.classic:
        drawRect(0, 0, 800, 800)
        drawLabel(str(app.userScore), 560, 440, size=50, fill='white')
        drawLabel(str(app.aiScore), 560, 360, size=50, fill='white')
        drawLine(10, 10, 10, 790, fill='cyan', lineWidth=10)
        drawLine(590, 10, 590, 790, fill='cyan', lineWidth=8)
        drawLine(10, 10, 200, 10, fill='cyan', lineWidth=8)
        drawLine(590, 10, 400, 10, fill='cyan', lineWidth=8)
        drawLine(10, 790, 200, 790, fill='cyan', lineWidth=8)
        drawLine(590, 790, 400, 790, fill='cyan', lineWidth=8)
        drawLine(10, 400, 590, 400, fill='cyan')
        drawCircle(300, 400, 75, fill=None, border='cyan')
        drawCircle(app.userX, app.userY, 50, fill='blue')

        drawCircle(app.userX, app.userY, 25, fill='blue', border='black')
        drawCircle(app.puckX, app.puckY, app.puckRadius, fill='red')

        drawCircle(app.aiX, app.aiY, 50, fill='green')
        drawCircle(app.aiX, app.aiY, 25, fill='green', border='black')
        if app.pause:
            drawLabel('SCORE!!!', 300, 200, size=80, fill='white')
            drawLabel(f'Game resumes in {str(app.counter)}', 300, 400, size=50, fill='white')
        if app.start:
            drawLabel(f'Game starts in {str(app.counter)}', 300, 400, size=50, fill='white')

def onMousePress(app, mouseX, mouseY):
    if not app.gameStart:
        if (app.easySelected or app.medSelected or app.hardSelected) and (225 <= mouseX <= 375) and (600 <= mouseY <= 675):
            app.gameStart = True
            startGame(app)
        if (75 <= mouseX <= 125) & (495 <= mouseY <= 505):
            app.easySelected = True
            app.medSelected = False
            app.hardSelected = False
            app.aiSpeed = 4
            app.aiMovementSpeed = 4
        if (275 <= mouseX <= 325) & (495 <= mouseY <= 505):
            app.easySelected = False
            app.medSelected = True
            app.hardSelected = False
            app.aiSpeed = 7
            app.aiMovementSpeed = 5
        if (475 <= mouseX <= 525) & (495 <= mouseY <= 505):
            app.easySelected = False
            app.medSelected = False
            app.hardSelected = True
            app.aiSpeed = 10
            app.aiMovementSpeed = 6
        
    if app.gameEnd and (225 <= mouseX <= 375) and (415 <= mouseY <= 490):
        app.gameStart = False
        app.gameEnd = False
        startGame(app)
        
def onMouseMove(app, mouseX, mouseY):
    if app.gameStart:
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
        # Update user paddle position
        dx = app.targetX - app.userX
        dy = app.targetY - app.userY
        app.userSpeed = math.sqrt(dx**2 + dy**2) * 0.2
        app.userX += dx * 0.5
        app.userY += dy * 0.5

        moveAIPaddle(app)
        checkAICollision(app)
        # if ((app.puckY - app.puckRadius <= 10) or (app.puckX - app.puckRadius <= 10) 
        #     or (app.puckX + app.puckRadius >= app.width - 10)):
        #     wait(app)
        # Update puck position
        app.puckX += app.puckVelocityX
        app.puckY += app.puckVelocityY
        
        # Check collision between paddle and puck
        distance = math.sqrt((app.userX - app.puckX)**2 + (app.userY - app.puckY)**2)
        if distance < 75:
            dx = app.puckX - app.userX
            dy = app.puckY - app.userY
            magnitude = math.sqrt(dx**2 + dy**2)
            if magnitude != 0:
                app.puckVelocityX = (dx / magnitude) * app.userSpeed * 3 
                app.puckVelocityY = (dy / magnitude) * app.userSpeed * 3
        
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

def moveAIPaddle(app):
    # Increase base speed from 4 to 6
    aiSpeed = 6  
    
    if app.puckY <= app.height / 2:  # React only when the puck is on AI's side
        # Add momentum prediction Amazon Q {
        predictedPuckX = app.puckX + app.puckVelocityX * (
            (app.aiY - app.puckY) / app.puckVelocityY if app.puckVelocityY != 0 else 0
        )
        
        # If puck is moving fast, increase prediction distance
        if abs(app.puckVelocityX) > 5 or abs(app.puckVelocityY) > 5:
            predictedPuckX += app.puckVelocityX * 2
        
        predictedPuckX = max(50, min(550, predictedPuckX))  # Stay within bounds
        # }
        if not(predictedPuckX < 25 or predictedPuckX > 575):
            app.aiTargetX = predictedPuckX
            # More aggressive Y targeting
            if app.puckY < app.height / 3:
                app.aiTargetY = app.puckY + app.puckVelocityY * 2  # Anticipate movement
            else:
                app.aiTargetY = app.puckY
    else:
        # Faster return to defensive position
        app.aiTargetX = app.width/2  # Center position instead of following puck
        app.aiTargetY = 150

    # Increase movement speed based on distance to target
    distanceToTarget = math.sqrt((app.aiTargetX - app.aiX)**2 + 
                               (app.aiTargetY - app.aiY)**2)
    
    # Boost speed when far from target
    if distanceToTarget > 100:
        aiSpeed = 8  # Extra speed when need to cover large distance
    
    # Move AI paddle towards the target position with increased speed
    if app.aiX < app.aiTargetX:
        app.aiX += min(aiSpeed, app.aiTargetX - app.aiX)  # Move right
    elif app.aiX > app.aiTargetX:
        app.aiX -= min(aiSpeed, app.aiX - app.aiTargetX)  # Move left

    if app.aiY < app.aiTargetY:
        app.aiY += min(aiSpeed, app.aiTargetY - app.aiY)  # Move down
    elif app.aiY > app.aiTargetY:
        app.aiY -= min(aiSpeed, app.aiY - app.aiTargetY)  # Move up

    # Keep AI paddle within bounds
    app.aiX = max(50, min(550, app.aiX))  # X boundary
    app.aiY = max(50, min(350, app.aiY))  # Y boundary



#Amazon Q{
def checkAICollision(app):
    # Calculate distance between AI paddle and puck
    distance = math.sqrt((app.aiX - app.puckX)**2 + (app.aiY - app.puckY)**2)
    if distance < 75:  # Collision threshold (paddle radius + puck radius)
        # Calculate collision normal
        collisionNormalX = (app.puckX - app.aiX) / distance
        collisionNormalY = (app.puckY - app.aiY) / distance

        currentSpeed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)

        minSpeed = 8

        if currentSpeed < 1 and app.puckX == 300 and app.puckY == 400:
            app.puckVelocityX = collisionNormalX * minSpeed
            app.puckVelocityY = collisionNormalY * minSpeed
        else:
        # Reflect puck velocity based on collision normal
            dotProduct = (app.puckVelocityX * collisionNormalX +
                        app.puckVelocityY * collisionNormalY)
            reflectedVelocityX = app.puckVelocityX - 2 * dotProduct * collisionNormalX
            reflectedVelocityY = app.puckVelocityY - 2 * dotProduct * collisionNormalY

            speedMultiplier = 1.2
            # newSpeed = math.sqrt(reflectedVelocityX**2 + reflectedVelocityY**2) * speedMultiplier
            # if newSpeed > minSpeed:
            #     speedMultiplier = minSpeed / newSpeed
            app.puckVelocityX = reflectedVelocityX * speedMultiplier
            app.puckVelocityY = reflectedVelocityY * speedMultiplier

        # Offset puck slightly to prevent overlap after collision
        overlap = 75 - distance
        app.puckX += collisionNormalX * overlap * 0.5
        app.puckY += collisionNormalY * overlap * 0.5

    # distance = math.sqrt((app.aiX - app.puckX)**2 + (app.aiY - app.puckY)**2)
    # if distance < 75 and app.lastHitTime + 0.1 < time.time():
    #     # Calculate the angle of collision
    #     relativeX = app.puckX - app.aiX
    #     relativeY = app.puckY - app.aiY
        
    #     # Calculate angle between puck and paddle center
    #     collisionAngle = math.atan2(relativeY, relativeX)
    #     # Determine if it's a side hit or front hit
    #     # Convert angle to degrees for easier comparison
    #     angleDegrees = math.degrees(collisionAngle)
    #     print(angleDegrees)
    #     if angleDegrees == 0 or angleDegrees == 180:
    #         speed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
    #         app.puckVelocityX = math.cos(random.randint(10, 30)) * speed * 1.2
    #         app.puckVelocityY = math.sin(random.randint(10, 30)) * speed * 1.2
    #         # backOff(app)
    #     # elif 0 < angleDegrees < 180:
    #     #     dx = app.puckX - app.userX
    #     #     dy = app.puckY - app.userY
    #     #     magnitude = math.sqrt(dx**2 + dy**2)
    #     #     if magnitude != 0:
    #     #         app.puckVelocityX = (dx / magnitude) * app.aiSpeed * 3 
    #     #         app.puckVelocityY = (dy / magnitude) * app.aiSpeed * 3
    #     #     # backOff(app) 
    #     elif -45 <= angleDegrees <= 45 or 135 <= angleDegrees <= 225:
    #         # Side hit - bounce based on collision angle
    #         print('Hit the side')
    #         speed = math.sqrt(app.puckVelocityX**2 + app.puckVelocityY**2)
    #         if speed == 0:
    #             speed = app.aiSpeed
                
    #         # Calculate new velocity based on collision angle
    #         app.puckVelocityX = math.cos(random.randint(10, 30)) * speed * 1.2
    #         app.puckVelocityY = math.sin(random.randint(10, 30)) * speed * 1.2
    #         # backOff(app)
    #     else:
    #         #Front hit - aim towards goal
    #         if app.puckY <= app.height / 2:
    #             goalCenterX = app.width / 2 + random.uniform(-50, 50)
            
    #         goalCenterY = app.height - app.goalHeight
            
    #         dx = goalCenterX - app.puckX
    #         dy = goalCenterY - app.puckY
            
    #         magnitude = math.sqrt(dx**2 + dy**2)
    #         if magnitude != 0:
    #             dx /= magnitude
    #             dy /= magnitude
            
    #         # Vary speed based on distance from paddle center
    #         hitAccuracy = 1 - (distance / 75)  # 1 at center, 0 at edge
    #         speed = app.aiSpeed * (3 + hitAccuracy)
            
    #         app.puckVelocityX = dx * speed
    #         app.puckVelocityY = dy * speed
    #     #     dx = app.puckX - app.userX
    #     #     dy = app.puckY - app.userY
    #     #     magnitude = math.sqrt(dx**2 + dy**2)
    #     #     if magnitude != 0:
    #     #         app.puckVelocityX = (dx / magnitude) * app.aiSpeed * 3 * -1
    #     #         app.puckVelocityY = (dy / magnitude) * app.aiSpeed * 3 * -1

    #     # app.lastHitTime = time.time()
# }

def backOff(app):
    app.aiY -= 30

def main():
    runApp()

main()