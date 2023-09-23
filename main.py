import pygame, math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
size = (int(224*2.5), int(288*2.5))
singleCellDimension = (int(size[0]/28), int(size[1]/36))

screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

done = False

gameGrid = [[(False, None, None) for x in range(28)] for y in range(36)]

def renderText(text, font, color):
    renderFont = pygame.font.Font(font, 36)
    renderedText = renderFont.render(text, False, color)
    transformedSurface = pygame.transform.scale(renderedText, (singleCellDimension[0] - 4, singleCellDimension[1] - 4))
    return transformedSurface

clock = pygame.time.Clock()

def writeText(text, font, color, coordinates):
    for letterIndex in range(len(text)):
        gameGrid[coordinates[1]][coordinates[0] + letterIndex] = (True, None, renderText(text[letterIndex], font, color))
    return True

def loadLevel(levelSchematic, coordinates):
    schematic = open(str(levelSchematic)).readlines()
    for placementY in range(len(schematic)):
        for placementX in range(len(schematic[placementY])):
            if schematic[placementY][placementX] == "1":
                gameGrid[placementY + coordinates[1]][placementX + coordinates[0]] = (True, None, renderText("[]", "PressStart2P.ttf", (0, 0, 255)))
            elif schematic[placementY][placementX] == "2":
                gameGrid[placementY + coordinates[1]][placementX + coordinates[0]] = (True, None, renderText("[]", "PressStart2P.ttf", (255, 255, 0)))


writeText("CURRENT SCORE", "PressStart2P.ttf", WHITE, (7, 0))
loadLevel("levelTemplate.pmlt", (0, 3))

pacmansPosition = [1, 4]
direction = "UP"

pacmanImage = pygame.transform.scale(pygame.image.load("Llamas.png"), (singleCellDimension[0] - 4, singleCellDimension[1] - 4))
detailedPosition = [float(pacmansPosition[0]), float(pacmansPosition[1])]

def locatePossibleAvenues(position):
    return (gameGrid[position[1] - 1][position[0]][0], gameGrid[position[1]][position[0] + 1][0],
            gameGrid[position[1] + 1][position[0]][0], gameGrid[position[1]][position[0] - 1][0])

def calculateDistance(pointA, pointB):
    return (((abs(pointB[0] - pointA[0]))**2) + ((abs(pointB[1] - pointA[1]))**2))**(1/2)

def locateVectorsFromPoint(position):
    intersectionPoints = locatePossibleAvenues(position)
    vectorLocations = []

    if not intersectionPoints[0]:
        for offsetY in range(1, 40):
            if not gameGrid[position[1] - offsetY][position[0]][0]:
                vectorLocations.append((position[0], position[1] - offsetY))
            else:
                break

    if not intersectionPoints[1]:
        for offsetX in range(1, 40):
            if not gameGrid[position[1]][position[0] + offsetX][0]:
                vectorLocations.append((position[0] + offsetX, position[1]))
            else:
                break

    if not intersectionPoints[2]:
        for offsetY in range(1, 40):
            if not gameGrid[position[1] + offsetY][position[0]][0]:
                vectorLocations.append((position[0], position[1] + offsetY))
            else:
                break

    if not intersectionPoints[3]:
        for offsetX in range(1, 40):
            if not gameGrid[position[1]][position[0] - offsetX][0]:
                vectorLocations.append((position[0] - offsetX, position[1]))
            else:
                break
    return vectorLocations

def analyseForOptimumPoint(points, target):
    currentDistance = 0
    for point in points:
        if True in locatePossibleAvenues:
            tempDistance = ((((point[0] - target[0])**2) + ((point[1] - target[1])**2))**(1/2))
            if tempDistance > currentDistance:
                currentDistance = tempDistance
    return currentDistance

def determineMovementMatrix(positionA, positionB):
    movementVector = (positionB[0] - positionA[0], positionB[1] - positionA[1])
    steps = []

    if movementVector[0] > 0:
        for i in range(abs(movementVector[0])): steps.append("RIGHT")
    elif movementVector[0] < 0:
        for i in range(abs(movementVector[0])): steps.append("LEFT")
    elif movementVector[1] > 0:
        for i in range(abs(movementVector[1])): steps.append("DOWN")
    elif movementVector[1] < 0:
        for i in range(abs(movementVector[1])): steps.append("UP")
    return steps
import time
def determineCorrectPath(pointA, pointB):
    pointX = pointA
    allSteps = []

    possibleLocations = locateVectorsFromPoint(pointX)

    closestIntersectionPoint = (200, 200)
    for point in possibleLocations:
        if locatePossibleAvenues(point) not in [(True, False, True, False), (False, True, False, True)]:
            if calculateDistance(point, pointB) < calculateDistance(closestIntersectionPoint, pointB):
                closestIntersectionPoint = point

    allSteps += determineMovementMatrix(pointX, closestIntersectionPoint)

    return allSteps

class Ghost:
    image = None
    pathFindingAlgorithm = None
    location = (0, 0)
    def UP(self):
        self.location = (self.location[0], self.location[1] - 1)
    def RIGHT(self):
        self.location = (self.location[0] + 1, self.location[1])
    def DOWN(self):
        self.location = (self.location[0], self.location[1] + 1)
    def LEFT(self):
        self.location = (self.location[0] - 1, self.location[1])

RedGhost = Ghost()
RedGhost.image = pygame.transform.scale(pygame.image.load("Oskar.png"), (singleCellDimension[0] - 4, singleCellDimension[1] - 4))
RedGhost.pathFindingAlgorithm = determineCorrectPath
RedGhost.location = (26, 4)
PinkGhost = Ghost()
PinkGhost.image = pygame.transform.scale(pygame.image.load("Kyle.png"), (singleCellDimension[0] - 4, singleCellDimension[1] - 4))
PinkGhost.pathFindingAlgorithm = determineCorrectPath
PinkGhost.location = (9, 20)
OrangeGhost = Ghost()
OrangeGhost.image = pygame.transform.scale(pygame.image.load("Phil.png"), (singleCellDimension[0] - 4, singleCellDimension[1] - 4))
OrangeGhost.pathFindingAlgorithm = determineCorrectPath
OrangeGhost.location = (1, 32)
BlueGhost = Ghost()
BlueGhost.image = pygame.transform.scale(pygame.image.load("Ben.png"), (singleCellDimension[0] - 4, singleCellDimension[1] - 4))
BlueGhost.pathFindingAlgorithm = determineCorrectPath
BlueGhost.location = (26, 32)

currentStep = 0
currentStep1 = 0
currentStep2 = 0
currentStep3 = 0
t = time.time()
import random
t1 = time.time()
calculatedSteps = determineCorrectPath(RedGhost.location, pacmansPosition)
RedGhostTemp = RedGhost.location
pacmanTemp = pacmansPosition
calculatedSteps1 = determineCorrectPath(PinkGhost.location, pacmansPosition)
PinkGhostTemp = PinkGhost.location
pacmanTemp1 = pacmansPosition
calculatedSteps2 = determineCorrectPath(OrangeGhost.location, pacmansPosition)
OrangeGhostTemp = OrangeGhost.location
pacmanTemp2 = pacmansPosition
calculatedSteps3 = determineCorrectPath(BlueGhost.location, pacmansPosition)
BlueGhostTemp = BlueGhost.location
pacmanTemp3 = pacmansPosition
pacmansPoints = 0

for blockX in range(len(gameGrid[0])):
        for blockY in range(len(gameGrid)):
            if gameGrid[blockY][blockX][0] == False and gameGrid[blockY][blockX][1] != "PCMN":
                gameGrid[blockY][blockX] = (False, True, None)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    writeText(str(pacmansPoints), "PressStart2P.ttf", WHITE, (21, 0))

    if pygame.key.get_pressed()[pygame.K_UP]:
        if not gameGrid[pacmansPosition[1] - 1][pacmansPosition[0]][0]:
            direction = "UP"
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if not gameGrid[pacmansPosition[1] + 1][pacmansPosition[0]][0]:
            direction = "DOWN"
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if not gameGrid[pacmansPosition[1]][pacmansPosition[0] + 1][0]:
            direction = "RIGHT"
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if not gameGrid[pacmansPosition[1]][pacmansPosition[0] - 1][0]:
            direction = "LEFT"

    if not gameGrid[pacmansPosition[1] - 1][pacmansPosition[0]][0] and direction == "UP":
        detailedPosition[1] -= 0.25
    if not gameGrid[pacmansPosition[1] + 1][pacmansPosition[0]][0] and direction == "DOWN":
        detailedPosition[1] += 0.25
    if not gameGrid[pacmansPosition[1]][pacmansPosition[0] + 1][0] and direction == "RIGHT":
        detailedPosition[0] += 0.25
    if not gameGrid[pacmansPosition[1]][pacmansPosition[0] - 1][0] and direction == "LEFT":
        detailedPosition[0] -= 0.25

    pacmansPosition = (int(detailedPosition[0]), int(detailedPosition[1]))
    gameGrid[pacmansPosition[1]][pacmansPosition[0]] = (False, "PCMN", pacmanImage)

    if gameGrid[17][1][1] == "PCMN" and direction == "LEFT":
        pacmansPosition = (25, 17)
        detailedPosition = [float(pacmansPosition[0]), float(pacmansPosition[1])]

    if gameGrid[17][25][1] == "PCMN" and direction == "RIGHT":
        pacmansPosition = (1, 17)
        detailedPosition = [float(pacmansPosition[0]), float(pacmansPosition[1])]

    for blockX in range(len(gameGrid[0])):
        for blockY in range(len(gameGrid)):
            if gameGrid[blockY][blockX][0]:
                screen.blit(gameGrid[blockY][blockX][2], (int((blockX*singleCellDimension[0]) + (singleCellDimension[0]/2)) - (gameGrid[blockY][blockX][2].get_width()/2),
                                                 int(blockY*singleCellDimension[1]) + (singleCellDimension[1]/2) - (gameGrid[blockY][blockX][2].get_height()/2)))
            elif gameGrid[blockY][blockX][1] == True:
                if blockY > 3 and blockY < 34:
                    pygame.draw.circle(screen, WHITE, (int((blockX*singleCellDimension[0]) + (singleCellDimension[0]/2)),
                                                 int((blockY*singleCellDimension[1]) + (singleCellDimension[1]/2))), 2)
            elif gameGrid[blockY][blockX][1] == "PCMN":
                if pacmansPosition != (blockX, blockY):
                    pacmansPoints += 10
                    gameGrid[blockY][blockX] = (False, False, None)
                else:
                    if direction == "RIGHT" or direction == "DOWN":
                        screen.blit(gameGrid[blockY][blockX][2], (int((blockX*singleCellDimension[0]) + (singleCellDimension[0]/2)) - (gameGrid[blockY][blockX][2].get_width()/2),
                                                          int((blockY*singleCellDimension[1]) + (singleCellDimension[1]/2) - (gameGrid[blockY][blockX][2].get_height()/2))))
                    else:
                        screen.blit(gameGrid[blockY][blockX][2], (int((blockX*singleCellDimension[0]) + (singleCellDimension[0]/2)) - (gameGrid[blockY][blockX][2].get_width()/2),
                                                          int((blockY*singleCellDimension[1]) + (singleCellDimension[1]/2) - (gameGrid[blockY][blockX][2].get_height()/2))))

    screen.blit(RedGhost.image, (int((RedGhost.location[0]*singleCellDimension[0]) + (singleCellDimension[0]/2)) - (RedGhost.image.get_width()/2),
                                int((RedGhost.location[1]*singleCellDimension[1]) + (singleCellDimension[1]/2) - (RedGhost.image.get_height()/2))))
    screen.blit(PinkGhost.image, (int((PinkGhost.location[0]*singleCellDimension[0]) + (singleCellDimension[0]/2)) - (PinkGhost.image.get_width()/2),
                                int((PinkGhost.location[1]*singleCellDimension[1]) + (singleCellDimension[1]/2) - (PinkGhost.image.get_height()/2))))
    screen.blit(OrangeGhost.image, (int((OrangeGhost.location[0]*singleCellDimension[0]) + (singleCellDimension[0]/2)) - (OrangeGhost.image.get_width()/2),
                                int((OrangeGhost.location[1]*singleCellDimension[1]) + (singleCellDimension[1]/2) - (OrangeGhost.image.get_height()/2))))
    screen.blit(BlueGhost.image, (int((BlueGhost.location[0]*singleCellDimension[0]) + (singleCellDimension[0]/2)) - (BlueGhost.image.get_width()/2),
                                int((BlueGhost.location[1]*singleCellDimension[1]) + (singleCellDimension[1]/2) - (BlueGhost.image.get_height()/2))))
    pygame.display.flip()
    if time.time() - t > 0.4:
        if currentStep >= len(calculatedSteps):
            calculatedSteps = determineCorrectPath(RedGhost.location, pacmansPosition)
            currentStep = 0
            RedGhostTemp = RedGhost.location
        {"UP": RedGhost.UP, "DOWN": RedGhost.DOWN, "RIGHT": RedGhost.RIGHT, "LEFT": RedGhost.LEFT}[calculatedSteps[currentStep]]()
        if currentStep1 >= len(calculatedSteps1):
            calculatedSteps1 = determineCorrectPath(PinkGhost.location, pacmansPosition)
            currentStep1 = 0
            PinkGhostTemp = PinkGhost.location
        {"UP": PinkGhost.UP, "DOWN": PinkGhost.DOWN, "RIGHT": PinkGhost.RIGHT, "LEFT": PinkGhost.LEFT}[calculatedSteps1[currentStep1]]()
        if currentStep2 >= len(calculatedSteps2):
            calculatedSteps2 = determineCorrectPath(OrangeGhost.location, pacmansPosition)
            currentStep2 = 0
            OrangeGhostGhostTemp = OrangeGhost.location
        {"UP": OrangeGhost.UP, "DOWN": OrangeGhost.DOWN, "RIGHT": OrangeGhost.RIGHT, "LEFT": OrangeGhost.LEFT}[calculatedSteps2[currentStep2]]()
        if currentStep3 >= len(calculatedSteps3):
            calculatedSteps3 = determineCorrectPath(BlueGhost.location, pacmansPosition)
            currentStep3 = 0
            BlueGhostTemp = BlueGhost.location
        {"UP": BlueGhost.UP, "DOWN": BlueGhost.DOWN, "RIGHT": BlueGhost.RIGHT, "LEFT": BlueGhost.LEFT}[calculatedSteps3[currentStep3]]()
        t = time.time()

        currentStep += 1
        currentStep1 += 1
        currentStep2 += 1
        currentStep3 += 1

    if BlueGhost.location == pacmansPosition or RedGhost.location == pacmansPosition or \
        OrangeGhost.location == pacmansPosition or PinkGhost.location == pacmansPosition:
        import sys
        sys.exit()
        print("Game Over. You acquired", str(pacmansPoints), "during this game.")

    if time.time() - t1 > 0.5:
        for blockX in range(len(gameGrid[0])):
            for blockY in range(len(gameGrid)):
                if int(random.randrange(0, int(len(gameGrid[0])*len(gameGrid) / 3))) == 4:
                    if gameGrid[blockY][blockX][0] == False and gameGrid[blockY][blockX][1] != "PCMN":
                        gameGrid[blockY][blockX] = (False, True, None)
        t1 = time.time()
    clock.tick(120)


pygame.quit()