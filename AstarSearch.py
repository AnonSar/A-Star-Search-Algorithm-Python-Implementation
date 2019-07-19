import math
from termcolor import colored


class Heap:

    def __init__(self):

        self.discovered = []

    # method for adding the givenItem to the heap
    def addToHeap(self, givenItem):

        self.discovered.append(givenItem)
        self.heapify()

    # method for getting the deep copy of the heap list
    def getHeap(self):

        return self.discovered

    # function for updating the cost of a node in the heap
    def updateNodeCostInHeap(self, currentNode, FValue, GValue, sourceNode):

        for node in self.discovered:

            if node.position == currentNode.position:

                node.f = FValue
                node.g = GValue
                node.parent = sourceNode
                self.heapify()

    # method to change the position of the elements in the heap in order to satisfy the heap property
    def heapify(self):

        for item in range(len(self.discovered)):

            # if the index is greater than or equal to 1 and the parent is greater than children, then swap
            while item >= 1 and self.discovered[item].f <= self.discovered[item//2].f:

                if self.discovered[item].f < self.discovered[item//2].f:

                    self.swap(self.discovered, item, item // 2)

                elif self.discovered[item].f == self.discovered[item//2].f:

                    if self.discovered[item].h < self.discovered[item//2].h:

                        self.swap(self.discovered, item, item // 2)

                item = item // 2

    # method to get the minimum item from the heap
    def minItemFromHeap(self):

        result = self.discovered.pop(0)
        self.heapify()
        return result

    # method for swapping the values in the heap
    def swap(self, heap, firstIndex, secondIndex):

        tempVal = heap[firstIndex]
        heap[firstIndex] = heap[secondIndex]
        heap[secondIndex] = tempVal


class Node:

    def __init__(self, parent, position):

        self.parent = parent
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

        return math.sqrt((currentNode.position[0] - targetNode.position[0])**2 + (currentNode.position[1] - targetNode.position[1])**2)
        # return abs(currentNode.position[0] - targetNode.position[0]) + abs(currentNode.position[1] - targetNode.position[1])

    # method for implementing the a star search algorithm
    def aStarSearch(self, source, target):

        # if the source and the target, are the same, then return an empty path with a cost of 0
        if source == target:

            return ([], 0)

        sourceX, sourceY = source[0], source[1]
        targetX, targetY = target[0], target[1]

        # if the coordinates of the source or the target node are negative, then return an empty path with a cost of 0
        if sourceX < 0 or sourceY < 0 or targetX < 0 or targetY < 0:

            print("The source or target is negative.")
            return ([], 0)

        # if the coordinates of the source or target are out of range i.e. more than or less than the height or the width of the map, then return an empty path with a cost of 0
        if (sourceX > self.height) or (targetX > self.height) or (sourceY > self.width) or (targetY > self.width):

            print("The source or target is out range of the map.")
            return ([], 0)

        # if the source is not walkable, then return an empty path with a cost of 0
        if self.map[sourceX][sourceY] != '.':

            print("The source is not walkable. (", self.map[sourceX][sourceY], ")")
            return ([], 0)

        # if the target is not walkable, then return an empty path with a cost of 0
        if self.map[targetX][targetY] != ".":

            print("The target is not walkable. (", self.map[targetX][targetY], ")")
            return ([], 0)

        sourceNode = Node(None, source)
        targetNode = Node(None, target)

        # initialising the discovered list as a heap and the finalized list as a normal list
        discovered = Heap()
        finalized = []

        discovered.addToHeap(sourceNode)

        numberOfNodes = 0

        # while the discovered heap is not empty
        while len(discovered.getHeap()) != 0:

            smallest_value_node = discovered.minItemFromHeap()
            finalized.append(smallest_value_node)

            # print(smallest_value_node.position)

            # we have reached the target node, then return the entire path with it's total cost
            if smallest_value_node.position == target:

                shortestPath = []

                currentNode = smallest_value_node
                totalCost = currentNode.f

                # tracing back to the source node in order to retrieve the path
                while currentNode is not None:

                    shortestPath = [currentNode.position] + shortestPath
                    currentNode = currentNode.parent

                return shortestPath, totalCost, numberOfNodes

            neighborNode = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

            for node in neighborNode:

                # getting the position of the current node
                nodePositionX, nodePositionY = smallest_value_node.position[0] + node[0], smallest_value_node.position[1] + node[1]

                # if the neighbouring node is out of range, then skip to next node
                if nodePositionX > self.height or nodePositionY > self.width or nodePositionY < 0 or nodePositionX < 0:

                    continue

                # if the neighbouring node is not walkable, then skip to next neighbouring node
                if self.map[nodePositionX][nodePositionY] != ".":

                    continue
                childNodePosition = (nodePositionX, nodePositionY)
                childNodeParent = smallest_value_node
                childNode = Node(childNodeParent, childNodePosition)

                firstFlagChecker = False

                # if child node is in the finalised list, then skip to the next node
                for finalizedNode in finalized:

                    if finalizedNode.position == childNodePosition:

                        firstFlagChecker = True

                        break

                if firstFlagChecker:

                    continue

                # if the child node is not in the finalized list and not in discovered list
                secondFlagChecker = True
                discoveredList = discovered.getHeap()

                # checking if the node is in the discovered list, if the node is in the discovered list then skip to the next node
                for discoveredNode in discoveredList:

                    if discoveredNode.position == childNodePosition:

                        secondFlagChecker = False

                        break

                # if the node is not in the discovered list, then compute the cost of that node and add it to the discovered list
                if secondFlagChecker:

                    # if the child node happens to be in the diagonal
                    if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                        # if we are moving in the upper right or bottom right corner, then check that there are not obstacles in the corners in order to avoid corner cutting
                        if (node == (1, 1) or node == (-1, 1)) and self.map[smallest_value_node.position[0]][smallest_value_node.position[1] + 1] == ".":

                            if node == (1, 1) and self.map[smallest_value_node.position[0] + 1][smallest_value_node.position[1]] == ".":

                                numberOfNodes += 1

                                childNode.g = childNodeParent.g + math.sqrt(2)
                                childNode.h = self.heuristic(childNode, targetNode)
                                childNode.f = childNode.g + childNode.h
                                discovered.addToHeap(childNode)

                            elif node == (-1, 1) and self.map[smallest_value_node.position[0] - 1][smallest_value_node.position[1]] == ".":

                                numberOfNodes += 1

                                childNode.g = childNodeParent.g + math.sqrt(2)
                                childNode.h = self.heuristic(childNode, targetNode)
                                childNode.f = childNode.g + childNode.h
                                discovered.addToHeap(childNode)

                        # if we are moving in the upper left or bottom left corner, then check that there are not obstacles in the corners in order to avoid corner cutting
                        elif (node == (1, -1) or node == (-1, -1)) and (self.map[smallest_value_node.position[0]][smallest_value_node.position[1] - 1] == "."):

                            if node == (1, -1) and self.map[smallest_value_node.position[0] + 1][smallest_value_node.position[1]] == ".":

                                numberOfNodes += 1

                                childNode.g = childNodeParent.g + math.sqrt(2)
                                childNode.h = self.heuristic(childNode, targetNode)
                                childNode.f = childNode.g + childNode.h
                                discovered.addToHeap(childNode)

                            elif node == (-1, -1) and self.map[smallest_value_node.position[0] - 1][smallest_value_node.position[1]] == ".":

                                numberOfNodes += 1

                                childNode.g = childNodeParent.g + math.sqrt(2)
                                childNode.h = self.heuristic(childNode, targetNode)
                                childNode.f = childNode.g + childNode.h
                                discovered.addToHeap(childNode)

                    # if the child node isn't at the diagonal of the current node
                    elif node == (1, 0) or node == (-1, 0) or node == (0, 1) or node == (0, -1):

                        numberOfNodes += 1

                        childNode.g = childNodeParent.g + 1
                        childNode.h = self.heuristic(childNode, targetNode)
                        childNode.f = childNode.g + childNode.h
                        discovered.addToHeap(childNode)

                # if the child node is not in the finalized list but it's in the discovered list, then check whether we are getting a better value for that node
                else:

                    # if the neighbouring node happens to be at the diagonal of the current node, then set the f value accordingly
                    if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                        childNodeCurrentGVal = childNodeParent.g + math.sqrt(2)
                        childNodeCurrentHVal = self.heuristic(childNode, targetNode)
                        childNodeCurrentFVal = childNodeCurrentHVal + childNodeCurrentGVal

                    # if the neighbouring node is not at the diagonal of the current node, then set the f value accordingly
                    else:

                        childNodeCurrentGVal = childNodeParent.g + 1
                        childNodeCurrentHVal = self.heuristic(childNode, targetNode)
                        childNodeCurrentFVal = childNodeCurrentHVal + childNodeCurrentGVal

                    heapList = discovered.getHeap()

                    for nodeIndex in heapList:

                        if nodeIndex.position == childNode.position and nodeIndex.f <= childNodeCurrentFVal:

                            break

                    # if we are getting a better f value for the current child node, then update that value accordingly for that node in the discovered list
                    else:

                        # if the neighbouring node happens to be at diagonal, then check for the corners accordingly and update the cost of that node in the discovered list
                        if node == (1, 1) or node == (1, -1) or node == (-1, 1) or node == (-1, -1):

                            if (node == (1, 1) or node == (-1, 1)) and (self.map[smallest_value_node.position[0]][smallest_value_node.position[1] + 1] == "."):

                                if node == (1, 1) and self.map[smallest_value_node.position[0] + 1][smallest_value_node.position[1]] == ".":

                                    discovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallest_value_node)

                                elif node == (-1, 1) and self.map[smallest_value_node.position[0] - 1][smallest_value_node.position[1]] == ".":

                                    discovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallest_value_node)

                            elif (node == (1, -1) or node == (-1, -1)) and (self.map[smallest_value_node.position[0]][smallest_value_node.position[1] - 1] == "."):

                                if node == (1, -1) and self.map[smallest_value_node.position[0] + 1][smallest_value_node.position[1]] == ".":

                                    discovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallest_value_node)

                                elif node == (-1, -1) and self.map[smallest_value_node.position[0] - 1][smallest_value_node.position[1]] == ".":

                                    discovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallest_value_node)

                        elif node == (1, 0) or node == (-1, 0) or node == (0, 1) or node == (0, -1):

                            discovered.updateNodeCostInHeap(childNode, childNodeCurrentFVal, childNodeCurrentGVal, smallest_value_node)

        print("No possible path exist from the given source to given target.")

        return ([], 0)


x = Graph()
x.buildGraph("arena.map")
# print(x.aStarSearch((36, 31), (19, 47)))

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

        result = x.aStarSearch((item[5], item[4]), (item[7], item[6]))

        if int(result[1]) == int(float(item[8][:-1])):

            successString = colored("Test Passed: ", "green")
            print(successString)
            print("The coordinates are SOURCE(", item[4], ",", item[5], ") , TARGET(", item[6], ",", item[7], ")", " || The result I'm getting: [", result[1], "] The result I should be getting: [", float(item[8][:-1]), "]")
            print("The Path is: ", result[0])
            print("The number of nodes that have been visited are:", result[2])
            correct += 1
            print("")

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
