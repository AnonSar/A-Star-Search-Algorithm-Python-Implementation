import math
from termcolor import colored


class Heap:

    def __init__(self):

        self.Discovered = []

    # method for adding the givenItem to the heap
    def addToHeap(self, givenItem):

        self.Discovered.append(givenItem)
        self.heapify()

    # method for getting the deep copy of the heap list
    def getHeap(self):

        return self.Discovered

    # function for updating the cost of a node in the heap
    def updateNodeCostInHeap(self, currentNode, fValue, gValue, sourceNode):

        for node in self.Discovered:

            if node.position == currentNode.position:

                node.g = gValue
                node.f = fValue
                node.parent = sourceNode
                self.heapify()

    # method to change the position of the elements in the heap in order to satisfy the heap property
    def heapify(self):

        for item in range(len(self.Discovered)):

            # if the index is greater than or equal to 1 and the parent is greater than children, then swap
            while item >= 1 and self.Discovered[item].f <= self.Discovered[item//2].f:

                if self.Discovered[item].f < self.Discovered[item//2].f:

                    self.swap(self.Discovered, item, item // 2)

                elif self.Discovered[item].f == self.Discovered[item//2].f:

                    if self.Discovered[item].h < self.Discovered[item//2].h:

                        self.swap(self.Discovered, item, item // 2)

                item = item // 2

    # method to get the minimum item from the heap
    def minItemInHeap(self):

        result = self.Discovered.pop(0)
        self.heapify()
        return result

    # method to get the value of the root element at the heap
    def rootItemAtHeap(self):

        return self.Discovered[0]

    # method for swapping the values in the heap
    def swap(self, heap, firstIndex, secondIndex):

        tempVal = heap[firstIndex]
        heap[firstIndex] = heap[secondIndex]
        heap[secondIndex] = tempVal


class Node:

    def __init__(self, parent, position):

        self.parent = parent
        self.secondParent = None
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0


class Graph:

    def __init__(self):

        self.map = []
        self.height = 0
        self.width = 0

    # method for building the map in the required format
    def buildGraph(self, filename):

        file = open(filename, "r")

        lineNumber = 0

        for line in file:

            lineNumber += 1

            # to record the height of the map
            if lineNumber == 2:

                line = line.replace("\n", "")
                line = line.split(" ")
                self.height = int(line[-1]) - 1

            # to record the width of the map
            elif lineNumber == 3:

                line = line.replace("\n", "")
                line = line.split(" ")
                self.width = int(line[-1]) - 1

            # condition to check whether we are only storing those lines from the map which are having their first character as a map terrain
            elif line[0] == "@" or line[0] == "T" or line[0] == ".":

                # checking if the line is having the new line character
                if line[-1] == "\n":

                    # if the line is having new line character, then append the entire line except the last character
                    self.map.append(line[:-1])

                else:

                    # if the line is not having new line character, then append the entire line
                    self.map.append(line)

    # method for calculating the heuristic (Euclidean Distance)
    def heuristic(self, currentNode, targetNode):

        # -------------Octile Heuristic------------------------------

        xVal = abs(currentNode.position[0] - targetNode.position[0])
        yVal = abs(currentNode.position[1] - targetNode.position[1])

        return max(xVal, yVal) + ((math.sqrt(2)-1)*min(xVal, yVal))

        # -------------Octile Heuristic------------------------------

        # -------------Euclidean Heuristic-------------------------

        # return math.sqrt((currentNode.position[0] - targetNode.position[0]) ** 2 + (currentNode.position[1] - targetNode.position[1]) ** 2)

        # -------------Euclidean Heuristic-------------------------

    # method for getting the node with minimum value from the either direction
    def minValueNodeFromEitherDirection(self, forwardDiscovered, backwardDiscovered, forwardFinalized, backwardFinalised):

        forwardMinItem = forwardDiscovered.rootItemAtHeap()
        backwardMinItem = backwardDiscovered.rootItemAtHeap()
        
        if forwardMinItem.f < backwardMinItem.f:
        
            result = forwardDiscovered.minItemInHeap()
            forwardFinalized.append(result)
            return result, "forward"
        
        elif forwardMinItem.f > backwardMinItem.f:
        
            result = backwardDiscovered.minItemInHeap()
            backwardFinalised.append(result)
            return result, "backward"
        
        elif forwardMinItem.f == backwardMinItem.f:
        
            if forwardMinItem.h > backwardMinItem.h:
        
                result = forwardDiscovered.minItemInHeap()
                forwardFinalized.append(result)
                return result, "forward"
        
            else:
        
                result = backwardDiscovered.minItemInHeap()
                backwardFinalised.append(result)
                return result, "backward"

    def minItemFromList(self, node, givenList):

        for item in givenList:

            if item.position == node.position:

                return True

            else:

                return False

    # method implementing bi-directional search algorithm
    def biDirectionalSearch(self, source, target):

        # if the source and the target, are the same, then return an empty path with a cost of 0
        if source == target:

            return ([], 0)

        sourceX, sourceY = source[0], source[1]
        targetX, targetY = target[0], target[1]

        # if the coordinates of the source or the target node are negative, then return an empty path with a cost of 0
        if sourceX < 0 or sourceY < 0 or targetX < 0 or targetY < 0:

            print("The source or target is negative.")
            return ([], 0)

        # if the coordinates of the source are out of range, then return an empty path with a cost of 0
        if (sourceX > self.height) or (sourceY > self.width):

            print("The source is out of range of the map.")
            return ([], 0)

        # if the coordinates of the target are out of range, then return an empty path with a cost of 0
        if (targetX > self.height) or (targetY > self.width):

            print("The target is out of range of the map.")
            return ([], 0)

        # if the source is not walkable, then return an empty path with a cost of 0
        if self.map[sourceX][sourceY] != ".":

            print("The source is not walkable. (", self.map[sourceX][sourceY], ")")
            return ([], 0)

        # if the target is not walkable, then return an empty path with a cost of 0
        if self.map[targetX][targetY] != ".":

            print("The target is not walkable. (", self.map[targetX][targetY], ")")
            return ([], 0)

        sourceNode = Node(None, source)
        targetNode = Node(None, target)

        # initialising the forwardDiscovered list as a heap and the finalized list as a normal list
        forwardDiscovered = Heap()
        forwardFinalized = []

        backwardDiscovered = Heap()
        backwardFinalised = []

        forwardDiscovered.addToHeap(sourceNode)
        backwardDiscovered.addToHeap(targetNode)

        numberOfNodes = 0

        while len(forwardDiscovered.getHeap()) != 0 and len(backwardDiscovered.getHeap()) != 0:

            # get the node with the smallest value from the either direction (forward or backward)
            smallestValueNode = self.minValueNodeFromEitherDirection(forwardDiscovered, backwardDiscovered, forwardFinalized, backwardFinalised)

            # if the smallest value node happens to be from the forward frontier
            if smallestValueNode[1] == "forward":

                # if the smallest value node happens to be from the forward frontier and it happens to be in the finalised list of the backward frontier
                if self.minItemFromList(smallestValueNode[0], backwardFinalised):

                    shortestPath = []

                    currentNode = smallestValueNode[0]
                    totalCost = currentNode.f

                    # tracing back to the source node in order to retrieve the path
                    while currentNode is not None:
                        shortestPath = [currentNode.position] + shortestPath
                        currentNode = currentNode.parent

                    return shortestPath, totalCost, numberOfNodes

                if True:

                    neighborNode = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

                    for node in neighborNode:

                        # getting the position of the current node
                        nodePositionX, nodePositionY = smallestValueNode[0].position[0] + node[0], smallestValueNode[0].position[1] + node[1]

                        # if the neighbouring node is out of range, then skip to next node
                        if nodePositionX > self.height or nodePositionY > self.width or nodePositionY < 0 or nodePositionX < 0:
                            continue

                        # if the neighbouring node is not walkable, then skip to next neighbouring node
                        if self.map[nodePositionX][nodePositionY] != ".":
                            continue

                        childNodePosition = (nodePositionX, nodePositionY)
                        childNodeParent = smallestValueNode[0]
                        childNode = Node(childNodeParent, childNodePosition)

                        firstFlagChecker = False

                        # if child node is in the finalised list, then skip to the next neighbouring node
                        for forwardFinalizedNode in forwardFinalized:

                            if forwardFinalizedNode.position == childNodePosition:

                                firstFlagChecker = True

                                break

                        if firstFlagChecker:

                            continue

                        # if the child node is not in the finalized list, then search the forwardDiscovered list
                        secondFlagChecker = True

                        forwardDiscoveredList = forwardDiscovered.getHeap()

                        # checking if the node is in the forwardDiscovered list, if the node is in the forwardDiscovered list then skip to the next node
                        for forwardDiscoveredNode in forwardDiscoveredList:

                            if forwardDiscoveredNode.position == childNodePosition:

                                secondFlagChecker = False

                                break

                        if secondFlagChecker:

                            # if the child node happens to be in the diagonal
                            if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                                # if we are moving in the upper right or bottom right corner, then check that there are not obstacles in the corners in order to avoid corner cutting
                                if (node == (1, 1) or node == (-1, 1)) and self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] + 1] == ".":

                                    if node == (1, 1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":

                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, targetNode)
                                        childNode.f = childNode.g + childNode.h
                                        forwardDiscovered.addToHeap(childNode)

                                    elif node == (-1, 1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":

                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, targetNode)
                                        childNode.f = childNode.g + childNode.h
                                        forwardDiscovered.addToHeap(childNode)

                                # if we are moving in the upper left or bottom left corner, then check that there are not obstacles in the corners in order to avoid corner cutting
                                elif (node == (1, -1) or node == (-1, -1)) and (self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] - 1] == "."):

                                    if node == (1, -1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":

                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, targetNode)
                                        childNode.f = childNode.g + childNode.h
                                        forwardDiscovered.addToHeap(childNode)

                                    elif node == (-1, -1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":

                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, targetNode)
                                        childNode.f = childNode.g + childNode.h
                                        forwardDiscovered.addToHeap(childNode)

                            # if the child node isn't at the diagonal of the current node
                            else:

                                numberOfNodes += 1

                                childNode.g = childNodeParent.g + 1
                                childNode.h = self.heuristic(childNode, targetNode)
                                childNode.f = childNode.g + childNode.h
                                forwardDiscovered.addToHeap(childNode)

                        # if the child node is not in the finalized list but it's in the forwardDiscovered list, then check whether we are getting a better value for that node
                        else:

                            # if the neighbouring node happens to be at the diagonal of the current node, then set the g value accordingly
                            if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                                childNodeCurrentGVal = childNodeParent.g + math.sqrt(2)
                                childNodeCurrentHVal = self.heuristic(childNode, targetNode)
                                childNodeCurrentFVal = childNodeCurrentHVal + childNodeCurrentGVal
    
                            # if the neighbouring node is not at the diagonal of the current node, then set the g value accordingly
                            else:

                                childNodeCurrentGVal = childNodeParent.g + 1
                                childNodeCurrentHVal = self.heuristic(childNode, targetNode)
                                childNodeCurrentFVal = childNodeCurrentHVal + childNodeCurrentGVal
    
                            for nodeIndex in forwardDiscovered.getHeap():
    
                                if nodeIndex.position == childNode.position and nodeIndex.f <= childNodeCurrentFVal:

                                    break
    
                            # if we are getting a better g value for the current child node, then update that value accordingly for that node in the forwardDiscovered list
                            else:
    
                                # if the neighbouring node happens to be at diagonal, then check for the corners accordingly and update the cost of that node in the forwardDiscovered list
                                if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):
    
                                    if (node == (1, 1) or node == (-1, 1)) and (self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] + 1] == "."):
    
                                        if node == (1, 1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":
    
                                            forwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])
    
                                        elif node == (-1, 1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":
    
                                            forwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])
    
                                    elif (node == (1, -1) or node == (-1, -1)) and (self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] - 1] == "."):
    
                                        if node == (1, -1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":
    
                                            forwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])
    
                                        elif node == (-1, -1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":
    
                                            forwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])
    
                                else:
    
                                    forwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])

            # if the smallest value node happens to be from the backward frontier
            elif smallestValueNode[1] == "backward":

                if self.minItemFromList(smallestValueNode[0], forwardFinalized):

                    shortestPath = []

                    currentNode = smallestValueNode[0]
                    totalCost = currentNode.f

                    # tracing back to the source node in order to retrieve the path
                    while currentNode is not None:

                        shortestPath = [currentNode.position] + shortestPath
                        currentNode = currentNode.parent

                    return shortestPath, totalCost, numberOfNodes

                if True:

                    neighborNode = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

                    for node in neighborNode:

                        # getting the position of the current node
                        nodePositionX, nodePositionY = smallestValueNode[0].position[0] + node[0], smallestValueNode[0].position[1] + node[1]

                        # if the neighbouring node is out of range, then skip to next node
                        if nodePositionX > self.height or nodePositionY > self.width or nodePositionY < 0 or nodePositionX < 0:
                            continue

                        # if the neighbouring node is not walkable, then skip to next neighbouring node
                        if self.map[nodePositionX][nodePositionY] != ".":
                            continue

                        childNodePosition = (nodePositionX, nodePositionY)
                        childNodeParent = smallestValueNode[0]
                        childNode = Node(childNodeParent, childNodePosition)

                        firstFlagChecker = False

                        # if child node is in the finalised list, then skip to the next neighbouring node
                        for backwardFinalizedNode in backwardFinalised:

                            if backwardFinalizedNode.position == childNodePosition:

                                firstFlagChecker = True

                                break

                        if firstFlagChecker:

                            continue

                        # if the child node is not in the finalized list, then search the backward frontier's discovered list
                        secondFlagChecker = True

                        backwardDiscoveredList = backwardDiscovered.getHeap()

                        # checking if the node is in the forwardDiscovered list, if the node is in the forwardDiscovered list then skip to the next node
                        for backwardDiscoveredNode in backwardDiscoveredList:

                            if backwardDiscoveredNode.position == childNodePosition:

                                secondFlagChecker = False

                                break

                        if secondFlagChecker:

                            # if the child node happens to be in the diagonal
                            if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                                # if we are moving in the upper right or bottom right corner, then check that there are not obstacles in the corners in order to avoid corner cutting
                                if (node == (1, 1) or node == (-1, 1)) and self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] + 1] == ".":

                                    if node == (1, 1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":

                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, sourceNode)
                                        childNode.f = childNode.g + childNode.h
                                        backwardDiscovered.addToHeap(childNode)

                                    elif node == (-1, 1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":

                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, sourceNode)
                                        childNode.f = childNode.g + childNode.h
                                        backwardDiscovered.addToHeap(childNode)

                                # if we are moving in the upper left or bottom left corner, then check that there are not obstacles in the corners in order to avoid corner cutting
                                elif (node == (1, -1) or node == (-1, -1)) and (self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] - 1] == "."):

                                    if node == (1, -1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":


                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, sourceNode)
                                        childNode.f = childNode.g + childNode.h
                                        backwardDiscovered.addToHeap(childNode)

                                    elif node == (-1, -1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":

                                        numberOfNodes += 1

                                        childNode.g = childNodeParent.g + math.sqrt(2)
                                        childNode.h = self.heuristic(childNode, sourceNode)
                                        childNode.f = childNode.g + childNode.h
                                        backwardDiscovered.addToHeap(childNode)

                            # if the child node isn't at the diagonal of the current node
                            else:

                                numberOfNodes += 1

                                childNode.g = childNodeParent.g + 1
                                childNode.h = self.heuristic(childNode, sourceNode)
                                childNode.f = childNode.g + childNode.h
                                backwardDiscovered.addToHeap(childNode)

                        # if the child node is not in the finalized list but it's in the forwardDiscovered list, then check whether we are getting a better value for that node
                        else:

                            # if the neighbouring node happens to be at the diagonal of the current node, then set the g value accordingly
                            if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                                childNodeCurrentGVal = childNodeParent.g + math.sqrt(2)
                                childNodeCurrentHVal = self.heuristic(childNode, targetNode)
                                childNodeCurrentFVal = childNodeCurrentHVal + childNodeCurrentGVal

                            # if the neighbouring node is not at the diagonal of the current node, then set the g value accordingly
                            else:

                                childNodeCurrentGVal = childNodeParent.g + 1
                                childNodeCurrentHVal = self.heuristic(childNode, targetNode)
                                childNodeCurrentFVal = childNodeCurrentHVal + childNodeCurrentGVal

                            for nodeIndex in forwardDiscovered.getHeap():

                                if nodeIndex.position == childNode.position and nodeIndex.f <= childNodeCurrentFVal:

                                    break

                            # if we are getting a better g value for the current child node, then update that value accordingly for that node in the forwardDiscovered list
                            else:

                                # if the neighbouring node happens to be at diagonal, then check for the corners accordingly and update the cost of that node in the forwardDiscovered list
                                if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                                    if (node == (1, 1) or node == (-1, 1)) and (self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] + 1] == "."):

                                        if node == (1, 1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":

                                            backwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])

                                        elif node == (-1, 1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":

                                            backwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])

                                    elif (node == (1, -1) or node == (-1, -1)) and (self.map[smallestValueNode[0].position[0]][smallestValueNode[0].position[1] - 1] == "."):

                                        if node == (1, -1) and self.map[smallestValueNode[0].position[0] + 1][smallestValueNode[0].position[1]] == ".":

                                            backwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])

                                        elif node == (-1, -1) and self.map[smallestValueNode[0].position[0] - 1][smallestValueNode[0].position[1]] == ".":

                                            backwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])

                                else:

                                    backwardDiscovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallestValueNode[0])

        print("No possible path exist from the given source to given target.")
        return ([], 0)


x = Graph()
x.buildGraph("arena.map")
# print(x.biDirectionalSearch((19, 26), (19, 29)))

file = open("arena.map.scen")

correct = 0
wrong = 0
unWalkable = 0
testCounter = 0

for item in file:

    item = item.split("\t")

    if len(item) > 2:

        testCounter += 1
        print("Test Case No. :", testCounter)

        item[4], item[5], item[6], item[7] = int(item[4]), int(item[5]), int(item[6]), int(item[7])

        result = x.biDirectionalSearch((item[5], item[4]), (item[7], item[6]))

        if int(result[1]) == int(float(item[8][:-1])):

            successString = colored("Test Passed: ", "green")
            print(successString)
            print("The coordinates are SOURCE(", item[4], ",", item[5], ") , TARGET(", item[6], ",", item[7], ")", " || The result I'm getting: [", result[1], "] The result I should be getting: [", float(item[8][:-1]), "]")
            print("The Path is: ", result[0])
            print("The number of nodes that have been visited are:", result[2])
            print("")
            correct += 1

        elif int(result[1]) == 0:

            unWalkablePath = colored("Test Failed: ", "blue")
            print(unWalkablePath)
            print("The coordinates are SOURCE(", item[4], ",", item[5], ") , TARGET(", item[6], ",", item[7], ")", " || The result I'm getting: [", result[1], "] The result I should be getting: [", float(item[8][:-1]), "]")
            unWalkable += 1
            print("")

        else:

            failureString = colored("Test Failed: ", "red")
            print(failureString)
            print("The coordinates are SOURCE(", item[4], ",", item[5], ") , TARGET(", item[6], ",", item[7], ")", " || The result I'm getting: [", result[1], "] The result I should be getting: [", float(item[8][:-1]), "]")
            print("The Path is: ", result[0])
            wrong += 1
            if len(result) == 3:

                print("The number of nodes that have been visited are:", result[2])

            print("")

print("Number of correct cases: ", correct)
print("Number of wrong cases: ", wrong)
print("Number of not walkable source issues: ", unWalkable)
