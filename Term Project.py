from cmu_graphics import *
import math

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
    app.aiTargetX = app.aiX 

    app.puckX = 300
    app.puckY = 400
    app.puckRadius = 25
    app.puckVelocityX = 0
    app.puckVelocityY = 0

    app.userScore = 0
    app.aiScore = 0

    app.counter = 3
    app.pause = False

    app.goalWidth = 200
    app.goalHeight = 20

    app.stepsPerSecond = 200

    app.gameEnd = False

    app.start = False

def redrawAll(app):
    if not app.gameStart:
        drawLabel("Single Player Air Hockey", 300, 200, size=40)
        drawLabel('Start', 300, 450, size=40)
        drawRect(225, 415, 150, 75, fill=None, border='black')
    elif app.gameEnd:
        if app.userScore > app.aiScore:
            drawLabel('You Won!', 300, 200, size=40)
        else:
            drawLabel('You Lost', 300, 200, size=40)
        drawLabel('Play Again', 300, 450)
        drawRect(225, 415, 150, 75, fill=None, border='black')
    else:
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
    if not app.gameStart and (225 <= mouseX <= 375) and (415 <= mouseY <= 490):
        app.gameStart = True
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

        # Update puck position
        app.puckX += app.puckVelocityX
        app.puckY += app.puckVelocityY
        
        # Check collision between paddle and puck
        distance = math.sqrt((app.userX - app.puckX)**2 + (app.userY - app.puckY)**2)
        if distance < 100:
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

        if (200 <= app.puckX <= 400) and (app.puckY - app.puckRadius <= app.goalHeight):  # Top goal
            app.userScore += 1
            if app.userScore == 5:
                app.gameEnd = True
            else:
                resetPuck(app)

        if (200 <= app.puckX <= 400) and (app.puckY + app.puckRadius >= app.height - app.goalHeight):  # Bottom goal
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
    # AI follows the puck's X position with some reaction time
    if app.puckY <= app.height / 2:  # Only react when the puck is on AI's side
        app.aiTargetX = app.puckX
        app.aiTargetY = app.puckY
    else:
        app.aiTargetX = app.puckX
        app.aiTargetY = 150
    # Move AI paddle towards its target position

    if app.puckY == app.aiY:
         app.aiTargetY = app.puckY - 25

    if app.aiX < app.aiTargetX:
        app.aiX += min(app.aiSpeed, app.aiTargetX - app.aiX)  # Move right
    elif app.aiX > app.aiTargetX:
        app.aiX -= min(app.aiSpeed, app.aiX - app.aiTargetX)  # Move left

    if app.aiY < app.aiTargetY:
        app.aiY += min(app.aiSpeed, app.aiTargetY - app.aiY)
    elif app.aiY > app.aiTargetY:
        app.aiY -= min(app.aiSpeed, app.aiY - app.aiTargetY)
    # Keep AI paddle within bounds
    app.aiX = max(50, min(550, app.aiX))  # Adjust based on paddle size
    app.aiX = max(50, min(350, app.aiY))

# Handle collisions between AI paddle and puck
def checkAICollision(app):
    distance = math.sqrt((app.aiX - app.puckX)**2 + (app.aiY - app.puckY)**2)
    if distance < 75:  # Collision threshold
        dx = app.puckX - app.aiX
        dy = app.puckY - app.aiY
        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude != 0:
            app.puckVelocityX = (dx / magnitude) * app.aiSpeed * 2
            app.puckVelocityY = (dy / magnitude) * app.aiSpeed * 2


def main():
    runApp()

main()