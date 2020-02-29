from PIL import Image
import math


class Node:
    def __init__(self, position, gCost, hCost, cost, parent=None):
        self.position = position
        self.parent = parent
        self.gCost = gCost
        self.hCost = hCost
        self.cost = cost


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


im = Image.open("terrain.png")
pic = im.load()

def summerTerrain():
    terrains = dict()
    terrains["(248,148,18)"] = 40
    terrains["(255,192,0)"] = 80
    terrains["(255,255,255)"] = 50
    terrains["(2,208,60)"] = 60
    terrains["(2,136,40)"] = 70
    terrains["(5,73,24)"] = 100
    terrains["(0,0,255)"] = 90
    terrains["(71,51,3)"] = 20
    terrains["(0,0,0)"] = 30
    terrains["(205,0,101)"] = 9999
    return terrains

def fallTerrain():
    terrains = dict()
    terrains["(248,148,18)"] = 40
    terrains["(255,192,0)"] = 80
    terrains["(255,255,255)"] = 60
    terrains["(2,208,60)"] = 70
    terrains["(2,136,40)"] = 80
    terrains["(5,73,24)"] = 100
    terrains["(0,0,255)"] = 90
    terrains["(71,51,3)"] = 20
    terrains["(0,0,0)"] = 30
    terrains["(205,0,101)"] = 9999
    return terrains

def winterTerrain():
    terrains = dict()
    terrains["(248,148,18)"] = 40
    terrains["(255,192,0)"] = 80
    terrains["(255,255,255)"] = 50
    terrains["(2,208,60)"] = 60
    terrains["(2,136,40)"] = 70
    terrains["(5,73,24)"] = 100
    terrains["(0,0,255)"] = 90
    terrains["(71,51,3)"] = 20
    terrains["(0,0,0)"] = 30
    terrains["(135,206,250)"] = 70
    terrains["(205,0,101)"] = 9999
    return terrains

def springTerrain():
    terrains = dict()
    terrains["(248,148,18)"] = 40
    terrains["(255,192,0)"] = 80
    terrains["(255,255,255)"] = 50
    terrains["(2,208,60)"] = 60
    terrains["(2,136,40)"] = 70
    terrains["(5,73,24)"] = 100
    terrains["(0,0,255)"] = 90
    terrains["(153,76,0)"] = 90
    terrains["(71,51,3)"] = 20
    terrains["(0,0,0)"] = 30
    terrains["(135,206,250)"] = 70
    terrains["(205,0,101)"] = 9999
    return terrains

def colorValueOfPixel(x, y, pic):
    pixelColor = str(pic[x, y])
    pixelColor = pixelColor[1:]
    pixelColor = pixelColor[:len(pixelColor) - 1]
    list = pixelColor.split(", ")
    list = list[:len(list) - 1]
    str1 = ','.join(str(e) for e in list)
    str1 = '(' + str1 + ')'
    return str1.strip()


def getMinNode(openList):
    min = 999999999
    for node in openList:
        if (node.cost < min):
            min = node.cost
            node1 = node

    openList.remove(node1)
    return node1, openList


def getChildren(position, nodeTracker):
    x = position.x
    y = position.y

    listOfChild = []
    if (x < 395 and y - 1 >= 0):
        childNode = Position(x, y - 1)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)
    if (x < 395 and y + 1 < 500):
        childNode = Position(x, y + 1)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)
    if (x + 1 < 395 and y < 500):
        childNode = Position(x + 1, y)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)
    if (x - 1 >= 0 and y < 500):
        childNode = Position(x - 1, y)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)
    if (x - 1 >= 0 and y - 1 >= 0):
        childNode = Position(x - 1, y - 1)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)
    if (x - 1 >= 0 and y + 1 < 500):
        childNode = Position(x - 1, y + 1)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)
    if (x + 1 < 395 and y - 1 >= 0):
        childNode = Position(x + 1, y - 1)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)
    if (x + 1 < 395 and y + 1 < 500):
        childNode = Position(x + 1, y + 1)
        if (not ("" + str(childNode.x) + str(childNode.y)) in nodeTracker):
            listOfChild.append(childNode)

    return listOfChild


def getHCost(childPosition, goal):
    x1 = childPosition.x
    x2 = goal.x
    y1 = childPosition.y
    y2 = goal.y

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def getGCost(currentGCost, position, childPosition, elevationMat, seasonId):
    if seasonId == 1:
        terrains = summerTerrain()
    elif seasonId == 2:
        terrains = fallTerrain()
    elif seasonId == 3:
        terrains = winterTerrain()
    elif seasonId == 4:
        terrains = springTerrain()

    childPixelColor = colorValueOfPixel(childPosition.x, childPosition.y, pic)
    terrainCost = terrains[childPixelColor]
    elevationCost = elevationMat[childPosition.y][childPosition.x] - elevationMat[position.y][position.x]
    totalGCost = currentGCost + terrainCost + elevationCost + 1

    return totalGCost


def aStar(start, goal, elevationMat, seasonId):
    openList = set()
    closedList = {}
    nodeTracker = {}

    node = Node(start, 0, getHCost(start, goal), getHCost(start, goal), None)
    openList.add(node)
    nodeTracker["" + str(start.x) + str(start.y)] = 1
    while (openList):
        node, openList = getMinNode(openList)

        position, gCost = node.position, node.gCost

        currentPos = "" + str(position.x) + " " + str(position.y)
        if currentPos in closedList:
            continue

        closedList[currentPos] = node.parent

        if (position.x == goal.x and position.y == goal.y):
            path = []
            path.append(currentPos)
            while ( currentPos ):
                currentPos = closedList[currentPos]
                path.append(currentPos)

            return path

        for childPosition in getChildren(position, nodeTracker):
            if not childPosition in closedList:
                childHCost = getHCost(childPosition, goal)
                childGCost = getGCost(gCost, position, childPosition, elevationMat, seasonId)
                childNode = Node(childPosition, childGCost, childHCost, childGCost + childHCost, currentPos)
                nodeTracker["" + str(childPosition.x) + str(childPosition.y)] = 1
                openList.add(childNode)

def isWaterBorder(x,y):
    if (x < 395 and y - 1 >= 0):
        color = colorValueOfPixel(x,y-1, pic)
        if (color != "(0,0,255)"):
            return True
    if (x < 395 and y + 1 < 500):
        color = colorValueOfPixel(x, y + 1, pic)
        if (color != "(0,0,255)"):
            return True
    if (x + 1 < 395 and y < 500):
        color = colorValueOfPixel(x + 1, y, pic)
        if (color != "(0,0,255)"):
            return True
    if (x - 1 >= 0 and y < 500):
        color = colorValueOfPixel(x - 1, y, pic)
        if (color != "(0,0,255)"):
            return True
    if (x - 1 >= 0 and y - 1 >= 0):
        color = colorValueOfPixel(x - 1, y - 1, pic)
        if (color != "(0,0,255)"):
            return True
    if (x - 1 >= 0 and y + 1 < 500):
        color = colorValueOfPixel(x - 1, y + 1, pic)
        if (color != "(0,0,255)"):
            return True
    if (x + 1 < 395 and y - 1 >= 0):
        color = colorValueOfPixel(x + 1, y - 1, pic)
        if (color != "(0,0,255)"):
            return True
    if (x + 1 < 395 and y + 1 < 500):
        color = colorValueOfPixel(x + 1, y + 1, pic)
        if (color != "(0,0,255)"):
            return True
    return False

def waterBorder():
    border = []
    for j in range (500):
        for i in range (395):
            if (colorValueOfPixel(i,j, pic) == "(0,0,255)"):
                if(isWaterBorder(i,j)):
                    border.append(Position(i,j))
    return border

def createElevationMatrix():
    file = open("mpp.txt", "r")
    elevationMat = [[0 for x in range(396)] for y in range(501)]
    lineNumber = 1
    for line in file:
        line = line.strip()
        elevations = line.split("   ")
        for i in range(395):
            elevationMat[lineNumber][i + 1] = float(elevations[i])
        lineNumber += 1
    return elevationMat

def getWinterNeighbours(x,y,pic):
    neighbour = []
    if (x < 395 and y - 1 >= 0):
        color = colorValueOfPixel(x,y-1, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x,y-1))
    if (x < 395 and y + 1 < 500):
        color = colorValueOfPixel(x, y + 1, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x, y + 1))
    if (x + 1 < 395 and y < 500):
        color = colorValueOfPixel(x + 1, y, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x+1, y))
    if (x - 1 >= 0 and y < 500):
        color = colorValueOfPixel(x - 1, y, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x-1, y))
    if (x - 1 >= 0 and y - 1 >= 0):
        color = colorValueOfPixel(x - 1, y - 1, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x - 1, y - 1))
    if (x - 1 >= 0 and y + 1 < 500):
        color = colorValueOfPixel(x - 1, y + 1, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x - 1, y + 1))
    if (x + 1 < 395 and y - 1 >= 0):
        color = colorValueOfPixel(x + 1, y - 1, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x + 1, y - 1))
    if (x + 1 < 395 and y + 1 < 500):
        color = colorValueOfPixel(x + 1, y + 1, pic)
        if (color == "(0,0,255)"):
            neighbour.append(Position(x + 1, y + 1))
    return neighbour

def getSpringNeighbours(x,y):
    neighbour = []
    if (x < 395 and y - 1 >= 0):
        color = colorValueOfPixel(x,y-1, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x,y-1))
    if (x < 395 and y + 1 < 500):
        color = colorValueOfPixel(x, y + 1, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x, y + 1))
    if (x + 1 < 395 and y < 500):
        color = colorValueOfPixel(x + 1, y, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x+1, y))
    if (x - 1 >= 0 and y < 500):
        color = colorValueOfPixel(x - 1, y, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x-1, y))
    if (x - 1 >= 0 and y - 1 >= 0):
        color = colorValueOfPixel(x - 1, y - 1, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x - 1, y - 1))
    if (x - 1 >= 0 and y + 1 < 500):
        color = colorValueOfPixel(x - 1, y + 1, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x - 1, y + 1))
    if (x + 1 < 395 and y - 1 >= 0):
        color = colorValueOfPixel(x + 1, y - 1, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x + 1, y - 1))
    if (x + 1 < 395 and y + 1 < 500):
        color = colorValueOfPixel(x + 1, y + 1, pic)
        if (color != "(0,0,255)" and color!= "(153,76,0)" and color != "(205,0,101)"):
            neighbour.append(Position(x + 1, y + 1))
    return neighbour

def bfs(queue, count, visited, season, elevationMat):
    if count == 0:
        return
    queue1 = []
    for pixel in queue:
        if (season == "winter"):
            neighbours = getWinterNeighbours(pixel.x, pixel.y, pic)
        elif (season == "spring"):
            neighbours = getSpringNeighbours(pixel.x, pixel.y)
        for point in neighbours:

            try:
                if visited[point] == 1:
                    continue
            except KeyError:
                if (season == "winter"):
                    pic[point.x, point.y] = (135, 206, 250)
                    queue1.append(point)
                    visited[point] = 1
                elif (season == "spring"):
                     if (elevationMat[point.y][point.x] - elevationMat[pixel.y][pixel.x]  < 1):
                        pic[point.x, point.y] = (153,76,0)
                        queue1.append(point)
                        visited[point] = 1

    bfs(queue1, count-1, visited, season, elevationMat)

def summerOrFall(checkPoints, elevationMat, seasonId):
    path = []
    pathLength = 0
    for i in range(len(checkPoints) - 1):
        start = checkPoints[i]
        goal = checkPoints[i + 1]
        path1 = aStar(start, goal, elevationMat, 4)
        pathLength = pathLength + len(path1)
        path = path + path1
    print("Total path length: ",pathLength)

    for way in path:
        if (way != None):
            way = way.strip().split(" ")
            pic[int(way[0]), int(way[1])] = (255, 0, 0)
    im.show()

def winter(checkPoints, elevationMat):

    numberOfPixels = 7
    visited = {}
    bfs(waterBorder(),numberOfPixels, visited, "winter", elevationMat)

    path = []
    pathLength = 0
    for i in range(len(checkPoints) - 1):
        start = checkPoints[i]
        goal = checkPoints[i + 1]
        path1 = aStar(start, goal, elevationMat, 4)  
        pathLength = pathLength + len(path1)
        path = path + path1
    print("Total path length: ",pathLength)
    for way in path:
        if (way != None):
            way = way.strip().split(" ")
            pic[int(way[0]), int(way[1])] = (255, 0, 0)
    im.show()

def spring(checkPoints, elevationMat):
    numberOfPixels = 15
    visited = {}
    bfs(waterBorder(), numberOfPixels, visited, "spring",elevationMat)

    path = []
    pathLength = 0
    for i in range(len(checkPoints) - 1):
        start = checkPoints[i]
        goal = checkPoints[i + 1]
        path1 = aStar(start, goal, elevationMat, 4)
        pathLength = pathLength + len(path1)
        path = path + path1
    print("Total path length: ",pathLength)
    for way in path:
        if (way != None):
            way = way.strip().split(" ")
            pic[int(way[0]), int(way[1])] = (255, 0, 0)
    im.show()



def main():

    elevationMat = createElevationMatrix()
    mapFile = open("brown.txt")

    checkPoints = []
    for line in mapFile:
        line = line.strip().split(' ')
        checkPoints.append(Position(int(line[0]), int(line[1])))

    print("Ids for different seasons:")
    print("Summer: 1")
    print("Fall: 2")
    print("Winter: 3")
    print("Spring: 4")
    seasonId = int(input("Enter Season Id: "))
    print()

    if seasonId == 1:
        summerOrFall(checkPoints, elevationMat, 1)
    elif seasonId == 2:
        summerOrFall(checkPoints, elevationMat, 2)
    elif seasonId == 3:
        winter(checkPoints, elevationMat)
    elif seasonId == 4:
        spring(checkPoints, elevationMat)

if __name__ == '__main__':
    main()
