from cmu_graphics import *
def onAppStart(app):
    app.squareSize = 100
    app.countIn = 0
    app.countOut = 0
    app.squareIsGrowing = True

def onMousePress(app, mouseX, mouseY):
    if (app.width/2-app.squareSize/2 < mouseX < app.width/2+app.squareSize/2) and (app.height/2-app.squareSize/2 < mouseY < app.height/2+app.squareSize/2):
        app.countIn += 1
        if app.squareSize == 250:
            app.squareSize -= 50
            app.squareIsGrowing = False
        elif app.squareSize == 50:
            app.squareSize += 50
            app.squareIsGrowing = True
        elif app.squareIsGrowing:
            app.squareSize += 50
        elif not app.squareIsGrowing:
            app.squareSize -= 50
    else:    
        app.countOut += 1

def redrawAll(app):
    if app.squareSize == 250 or app.squareSize == 50:
        fillColor = 'red'
    else:
        fillColor = 'lightGreen'
    drawLabel('Clicks inside the square: '+str(app.countIn), 200, 30, fill='black', font='arial')
    drawLabel('Clicks outside the square: '+str(app.countOut), 200, 60, fill='black', font='arial')
    drawRect(app.width/2-app.squareSize/2, app.height/2-app.squareSize/2, app.squareSize, app.squareSize, fill=fillColor)

def main():
    runApp()

main()