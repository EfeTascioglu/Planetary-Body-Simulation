# https://astro.unl.edu/naap/esp/centerofmass.html
class body:
    def __init__ (self, colour, mass, velocity, radius, loc):
        self.x = loc[0]
        self.y = loc[1]
        self.incrX = velocity[0]
        self.incrY = velocity[1]
        self.mass = mass
        self.rad = radius
        self.colour = colour
        
    def __str__ (self):
        return "(" +  str(self.x) + "," + str(self.y) + ")" + "\tMass:" + str(self.mass) + "\t\tRad:" + str(self.rad)
    
    def distTo(self, body2):
        return ( (body2.x - self.x)**2 + (body2.y - self.y)**2 ) **0.5
    def componentsTo(self, body2, speed): # Returns the IncrX and IncrY needed for self to move toward body2 at given speed
        speedAccelerant = ( ((speed)**2) / (( (body2.x - self.x)**2 ) +  (body2.y - self.y)**2 )) ** 0.5
        return speedAccelerant
    
    def isColliding(self, body2):
        distance = self.distTo(body2)
        #distToBeSwallowed = max(self.rad, body2.rad)
        return distance < self.rad + body2.rad
        
    def display(self):
        stroke(0)
        strokeWeight(1)
        fill(self.colour[0], self.colour[1], self.colour[2])
        ellipse(self.x, self.y, self.rad * 2, self.rad * 2)
        
    def travel(self):
        self.x, self.y = self.x + self.incrX, self.y + self.incrY
        
    def attraction(self, body2, G):
        distance = self.distTo(body2)
        
        force = (G * body2.mass * self.mass) / (distance ** 2)
        accelerationSelf = force / self.mass
        accelerationBody2 = force / body2.mass
        #acceleration = (G * body2.mass) / (distance ** 2)
        
        coeficiant1 = self.componentsTo(body2, accelerationSelf)
        self.incrX += (body2.x - self.x) * coeficiant1
        self.incrY += (body2.y - self.y) * coeficiant1
        
        coeficiant2 = body2.componentsTo(self, accelerationBody2)
        body2.incrX += (self.x - body2.x) * coeficiant2
        body2.incrY += (self.y - body2.y) * coeficiant2
    
    def collisionLogic(self, body2):
        totalMass = self.mass + body2.mass                  # Can you divide momentum into x & y components?????
        F1 = [self.incrX * self.mass, self.incrY * self.mass]
        F2 = [body2.incrX * body2.mass, body2.incrY * body2.mass]
        Fnew = [F1[0] + F2[0], F1[1] + F2[1]]
        velocity = [Fnew[0] / totalMass, Fnew[1] / totalMass]
        totalVolume = (PI * (self.rad ** 3) * 4/3) + (PI * (body2.rad ** 3) * 4/3)
        newRad = ((totalVolume * 3/4) / PI) ** (1.0/3.0)
        if self.mass > body2.mass:
            colour = self.colour
        else:
            colour = body2.colour
        newCoords = centerOfMass([self, body2], 2)
        return body(colour, totalMass, velocity, newRad, newCoords)
    
    def changeColour(self, colour):
        self.colour = colour
        self.display()

def centerOfMass(allBodies, bodyNum):
    centerOfMassX = 0
    centerOfMassY = 0
    totalMass = 0
    for i in range(bodyNum):
        centerOfMassX += allBodies[i].x * allBodies[i].mass
        centerOfMassY += allBodies[i].y * allBodies[i].mass
        totalMass += allBodies[i].mass
    centerOfMassX = centerOfMassX / totalMass
    centerOfMassY = centerOfMassY / totalMass
    return centerOfMassX, centerOfMassY

def loadInfoFromFile(fileName):
    try:
        file = open(fileName)
        myArray = []
        text = file.readlines()
        
        for line in text:
            line = line.strip() #Gets rid of end-of-line markers, etc.
            row = ""
            for c in line:
                row = row + c
            myArray.append(row.split(","))
        return myArray
    except IOError:
        print("Please include:", fileName, "in the Data folder")
    finally:
        file.close()
'''
def findLine(x1, x2, y1, y2):
    if x1 != x2:
        return (( float(y2 - y1) / (x2 - x1) ), y1 - (float(x1 * (y2 - y1)) / (x2 - x1)))
    else:
        return (None, None)

def area(x1, y1, x2, y2, x3, y3):
    myArea = (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
    if myArea < 0:
        myArea = myArea * -1
    return myArea
'''

import os
import time
import random
def setup():
    size(800, 800)
    global lastTime, frameTime, allColours, allBodies, bodyNum
    background(0)
    allData = []
    allColours = []
    lastTime = time.time()
    frameTime = 0.03 # 1 second in simulation is ***s in real life
    allBodies = []
    
    # Physics
    global G
    G = 100
    
    # Display
    global centerX, centerY, zoom, viewX, viewY
    centerX = 0
    centerY = 0
    zoom = 1
    viewX = 0
    viewY = 0
    
    format = "CASE"

    if format == "CASE":
        caseFile = "case1.txt" # !!!!!!!!!
        allData = []
        unFormattedData = loadInfoFromFile(caseFile)
        bodyNum = len(unFormattedData)
        for i in range(bodyNum):
            unFormattedData[i] = list(map(float, unFormattedData[i]))
            allData.append([unFormattedData[i][0:3]] + [unFormattedData[i][3]] + [unFormattedData[i][4:6]] + [unFormattedData[i][6]] + [unFormattedData[i][7:]])
            
        print(allData)    
    
    elif format == "RANDOM":
        bodyNum = 300 # !!!!!!!!!
        allData = []
        prevLocations = []
        for i in range(bodyNum):
            colour = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]
            mass = random.randint(1, 1)
            rad = random.randint(5, 5)
            velocity = [random.randint(-5, 5), random.randint(-5, 5)]
            location = [random.randint(-200, 1000), random.randint(-200, 1000)]
            while location in prevLocations:
                print("Planet in Planet: Regenerating")
                location = [random.randint(100, 700), random.randint(100, 700)]
            prevLocations.append(location)
            allData.append([colour, mass, velocity, rad, location])
            
    
    for i in range(bodyNum):
        allBodies.append(body(allData[i][0], allData[i][1], allData[i][2], allData[i][3], allData[i][4]))
        
def mouseWheel(event):
    global zoom
    e = event.getCount()
    zoom = zoom * (1 - 0.1 * e)
    zoom = max(zoom, 0.05)
    #print(zoom)

    
      
def draw():
    global lastTime, frameTime, allColours, allBodies, bodyNum
    global G
    global centerX, centerY, zoom, viewX, viewY
    
    if time.time() - lastTime >= frameTime:
        lastTime = time.time()
        background(0)
        
        # Moving the screen to keep the center of mass of the system at the center of the screen
        centerX, centerY = centerOfMass(allBodies, bodyNum)
        centerX -= 400 / zoom
        centerY -= 400 / zoom
        scale(zoom)
        translate(-centerX, -centerY)
        
        # The Scroll code (everything with zoom in it) took 2 hours to debug
                
        
        for i in range(bodyNum):
            allBodies[i].travel()
            
        for i in range(bodyNum): # Do acceleration separate to keep symmetry
            for j in range(i + 1, bodyNum):
                allBodies[i].attraction(allBodies[j], G)
        
        collision = True
        while collision:
            collision = False
            for i in range(bodyNum):
                for j in range(i+1, bodyNum):
                    if allBodies[i].isColliding(allBodies[j]):
                        allBodies.append(allBodies[i].collisionLogic(allBodies[j]))
                        allBodies.pop(j)
                        allBodies.pop(i)
                        bodyNum -= 1
                        collision = True
                        break
                if collision:
                    break
                    
        for i in range(bodyNum):
            #print(allBodies[i])
            allBodies[i].display()
        
            
        '''
        message, tri1, tri2 = testCases[caseNum]
        colour = [int(random(63, 255)) for i in range(3)]
        tri1 = Triangle(colour, tri1[0], tri1[1], tri1[2])
        colour = [int(random(63, 255)) for i in range(3)]
        tri2 = Triangle(colour, tri2[0], tri2[1], tri2[2])
        tri1.display()
        tri2.display()
        
        print(message)
        if tri1.isColliding(tri2):
            tri1.changeColour(colour)
            print("The Triangles Collide")
        else:
            print("The Triangles Don't Collide")
        '''
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
# This is just a test case used to debug some errors in the code  
"""
def initGame():
    global lastTime, allTriangles, allColours, numTriangles
    colour = [int(random(63, 255)) for i in range(3)]
    tri1 = Triangle(colour, [100, 300], [500, 700], [700, 700])
    tri1.display()
    colour = [int(random(63, 255)) for i in range(3)]
    tri2 = Triangle(colour, [100, 301], [499, 700], [100, 500])
    tri2.display()
    print(tri1.isColliding(tri2))
    
    
"""

#Create a rectangular boundaries, usable anywhere
"""
def areaBounds(collumnCount, rowCount, startX, startY, totalWidth, totalHeight, tileGaps):
    boundariesArray = []
    y = startY
    
    PicWid = totalWidth / collumnCount
    PicHei = totalHeight / rowCount
    for i in range ( rowCount ):
        x = startX
        for j in range (collumnCount):
            
            upperLeft = [ x, y ]                                        
            lowerRight = [ x + PicWid, y + PicHei ]
            clickBoundary = [ upperLeft, lowerRight ]
            boundariesArray.append( clickBoundary )
            x += (PicWid + tileGaps)
        y += (PicHei + tileGaps)    
    return boundariesArray
"""


#Use Anywhere, returns the picture if it exists
"""
def loadPic(picName):
    #print(os.listdir('./Data'))
    if(picName in os.listdir('./Data')):
        myPic = loadImage(picName)
        return myPic
    else:
        print("A Picture is Missing")
        print("Error in: " + picName)
"""   
''' 
def mouseReleased():
    global allBoundaries, whichSquare, removeSquare, activeAreas
    
#  all Boundaries is a list of tuples,  each tuple is the upper left and lower right of each box
#  if removeSquare is True, you will not be able to click again in that square again as that place in activeSquares will be turned to False
    whichSquare = - 1
    keepGoing = False
    for i in range( len(allBoundaries) ):
        if activeAreas[i]:
            validXRange = allBoundaries[i][0][0] <= mouseX <= allBoundaries[i][1][0] 
            validYRange = allBoundaries[i][0][1]  <= mouseY <= allBoundaries[i][1][1]
            validLocation = validXRange and validYRange
            if validLocation:
                whichSquare = i
                keepGoing = True
                break
'''
      
 
 
#Button Names is an array containing the names of all the buttons on the bottom bar
'''
def drawScrollingMenu(buttonNames, menuStartHeight, menuHeight, numButtons, allBoundaries, back, menuRevealed):
    
    try:
        # Test to see if Back is a colour
        if ( mouseY > menuStartHeight ) and not(menuRevealed):
        menuRevealed = True  
        textSize(50)
        for i in range(numButtons):
            fill(255)
            rect(allBoundaries[i][0][0],allBoundaries[i][0][1], allBoundaries[i][1][0] - allBoundaries[i][0][0], allBoundaries[i][1][1] - allBoundaries[i][0][1])
            fill(0)
            text(buttonNames[i], allBoundaries[i][0][0], (allBoundaries[i][1][1] + allBoundaries[i][0][1] ) / 2)
    elif ( mouseY < menuStartHeight ) and menuRevealed:
        menuRevealed = False
        fill(back[0], back[1], back[2])
        noStroke()
        rect(allBoundaries[0][0][0], allBoundaries[0][0][1], allBoundaries[numButtons][1][0] - allBoundaries[0][0][0], allBoundaries[numButtons][1][1] - allBoundaries[0][0][1])
        
    except IOError:
        # If it is not a colour...
        if ( mouseY > menuStartHeight ) and not(menuRevealed):
            menuRevealed = True  
            textSize(50)
            for i in range(numButtons):
                fill(255)
                rect(allBoundaries[i][0][0],allBoundaries[i][0][1], allBoundaries[i][1][0] - allBoundaries[i][0][0], allBoundaries[i][1][1] - allBoundaries[i][0][1])
                fill(0)
                text(buttonNames[i], allBoundaries[i][0][0], (allBoundaries[i][1][1] + allBoundaries[i][0][1] ) / 2)
        elif ( mouseY < menuStartHeight ) and menuRevealed:
            menuRevealed = False
            drawBackground(allBoundaries[0][0][0], allBoundaries[0][0][1], allBoundaries[numButtons-1][1][0], allBoundaries[numButtons-1][1][1])
'''

'''
def drawBackground(startX, startY, endX, endY):
    global back
    #print(endY)
    copy(back, 1920 * startX / width, 1080 * startY / height , 1920 * ( endX - startX ) / width, 1080 * ( endY - startY ) / height, startX ,startY ,endX - startX ,endY - startY)
'''

'''    
def displayText( word, wordSize, colour, x, y, thisWidth, thisHeight ):
    textSize(wordSize)
    if len(colour) == 1:
        fill(colour[0])
    elif len(colour) == 3:
        fill(colour[0], colour[1], colour[2])
    else:
        fill(colour[0], colour[1], colour[2], colour[3])
    text( word, x, y, thisWidth, thisHeight )
'''
