from dsets import DSet
import random
from Queue import Queue
import pdb
import json
from sets import Set
import pprint
import png
import Image
from time import sleep
import time

def abs(num):
    if num < 0:
        return -1 * num
    else:
        return num

class Map:

    def __init__(self, size, n):
        self.__map = list()

        for y in range(0, size):
            row = list()
            for x in range(0, size):
                temp = dict(connected=list())
                row.append(temp)
            self.__map.append(row)

        self.__dset = DSet(size * size)
        self.__size = size
        self.__edges = []
        self.__first = (-1, -1)
        self.generate(n)
        self.__edgeList = self.makeEdgeList()

    def getInitialPoint(self):
        return self.__first

    def getEdges(self, point):
        return self.__edgeList[str(point)]

    def generate(self, _n):
        self.__first = first = self.__getPoint()
        self.n = n = _n
        vertices = Set()

        while (n):
            second = self.__findClosestPoint(first)

            if not second in vertices:
                n -= 1
                vertices.add(second)

            if not second == (-1,-1):
                self.__dset.union(first[1] * self.__size + first[0], second[1] * self.__size + second[0])

                self.__map[first[0]][first[1]]['connected'].append(second)
                self.__map[second[0]][second[1]]['connected'].append(first)

                self.__edges.append((first, second))
                first = second
            else:
                break

    def printJSON(self, filename):
        for row in self.__map:
            for elem in row:
                print elem,
            print ""

        for segment in self.__edges:
            print str(segment[0]) + "->" + str(segment[1])

        with open(filename, 'w') as f:
            graph = list()
            output = {}

            output['size'] = self.__size
            for row in self.__map:
                for elem in row:
                    graph.append(elem)

            output['graph'] = graph
            output['edges'] = self.makeEdgeList()

            f.write(json.dumps(output))

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(output)

        graphPNG = []
        offset = 20
        for y in range(0, self.__size * offset):
            temp = []
            for x in range(0, self.__size * offset):
                temp.append(255)
            graphPNG.append(temp)

        edgeList = self.makeEdgeList()

        for vertex, edges in edgeList.iteritems():
            points = vertex.strip('(,)')
            points = points.split(' ')
            points[0] = points[0][0:1]

            for y in range(int(points[0]) * offset + 5, offset * (int(points[0]) + 1) - 5):
                for x in range(int(points[1]) * offset + 5, offset * (int(points[1]) + 1) - 5):
                    graphPNG[x][y] = 0

            for edge in edges:
                print points
                points[0] = int(points[0])
                points[1] = int(points[1])
                points[0] = points[0] * offset + offset/10
                points[1] = points[1] * offset + offset/10

                temp = [''] * 2
                temp[0] = edge[0] * offset + offset/10
                temp[1] = edge[1] * offset + offset/10

                edge = temp

                denom = (edge[0] - points[0])

                if (denom == 0):
                    slopeX = 0
                else:
                    slopeX = (edge[1] - points[1])/(edge[0] - points[0])

                print points,
                print ' destination ',
                print temp
                if (slopeX == 0):
                    slopeY = 1
                else:
                    slopeY = 1/slopeX
                currX = points[0]
                currY = points[1]

                while (not int(currX) == edge[0] and not int(currY) == edge[1]):
                    currX += slopeX
                    currY += slopeY

                    # print str(currX) + ', ' + str(currY) + ' destination is ' + str(temp) + ' and slope is ' + str(slopeX)
                    graphPNG[int(currX)][int(currY)] = 0

                png.from_array(graphPNG, 'L').save(filename.strip('.json') + '.png')

            return

    def makeEdgeList(self):
        edgeList = {}
        for edge in self.__edges:
            if not str(edge[0]) in edgeList:
                edgeList[str(edge[0])] = list()
            edgeList[str(edge[0])].append(edge[1])

            if not str(edge[1]) in edgeList:
                edgeList[str(edge[1])] = list()
            edgeList[str(edge[1])].append(edge[0])

        return edgeList

    def getCoordinate(self, coord):
        return coord[1] * self.__size + coord[0]

    def __findClosestPoint(self, first):
        nextPoint = Queue()
        nextPoint.put(first)
        visited = Set()

        while not nextPoint.empty():
            temp = nextPoint.get()

            # If already visited then you don't want to visit it again
            if temp in visited:
                continue

            visited.add(temp)

            if not temp == first:
                # If not connected and doesn't intersect
                if (not self.connected(first, temp) and
                    not self.doesIntersect(first, temp)):
                    return temp

            if temp[0] - 1 >= 0 and temp[1] - 1 >= 0:
                nextPoint.put((temp[0] - 1, temp[1] - 1))
            if temp[0] - 1 >= 0 and temp[1] + 1 < self.__size:
                nextPoint.put((temp[0] - 1, temp[1] + 1))
            if temp[0] + 1 < self.__size and temp[1] - 1 >= 0:
                nextPoint.put((temp[0] + 1, temp[1] - 1))
            if temp[0] + 1 < self.__size and temp[1] + 1 < self.__size:
                nextPoint.put((temp[0] + 1, temp[1] + 1))
            if temp[1] + 1 < self.__size:
                nextPoint.put((temp[0], temp[1] + 1))
            if temp[0] + 1 < self.__size:
                nextPoint.put((temp[0] + 1, temp[1]))
            if temp[1] - 1 >= 0:
                nextPoint.put((temp[0], temp[1] - 1))
            if temp[0] - 1 >= 0:
                nextPoint.put((temp[0] - 1, temp[1]))

        return (-1,-1)

    # Returns true if first or second is in the respective connected list
    # False if its not in either one
    def connected(self, first, second):
        return (first in self.__map[second[0]][second[1]]['connected'] or
                second in self.__map[first[0]][first[1]]['connected'])

    def __getPoint(self):
        x = random.randint(0, self.__size - 1)
        y = random.randint(0, self.__size - 1)

        return (x, y)

    # From http://paulbourke.net/geometry/pointlineplane/
    def doesIntersect(self, start, end):
        mua = 0.0
        mub = 0.0

        denom = 0.0
        numera = 0.0
        numerb = 0.0

        x1 = start[0]
        y1 = start[1]

        x2 = end[0]
        y2 = end[1]

        EPS = 0.0
        intersect = False

        for edge in self.__edges:
            x3 = edge[0][0]
            y3 = edge[0][1]

            x4 = edge[1][0]
            y4 = edge[1][0]

            denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
            numera = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
            numerb = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)

            if (abs(numera) <= EPS and
                abs(numerb) <= EPS and
                abs(denom) <= EPS):
                return True

            if (abs(denom) <= EPS):
                continue
            else:
                mua = numera/denom
                mub = numerb/denom

                if (mua < 0 or mua > 1 or mub < 0 or mub > 1):
                    continue
            return False

        return intersect

def ColorMap(randomMap):
    colors = ['R', 'G', 'B', 'Y']
    initialPoint = randomMap.getInitialPoint()
    visited = Set()
    nodeTree = dict()
    edgeList = randomMap.makeEdgeList()

    for point, edges in edgeList.iteritems():
        nodeTree[point] = colorNode('N', point, edges)

    avgEdges = 0
    for point, edges in edgeList.iteritems():
        avgEdges += len(edges)


    _ColorMap(currMap=randomMap, curr=initialPoint, tree=nodeTree, visited=visited, colors=colors)

    avgEdges /= randomMap.n
    nodeTree['avgEdges'] = avgEdges
    return nodeTree
    pass

class colorNode:

    def __init__(self, color, point, edges):
        self.color = color
        self.point = point
        self.edges = edges
        self.visitedNum = 0

def _ColorMap(currMap, curr, tree, visited, colors):
    remaining = False
    visited.add(curr)

    for point, node in tree.iteritems():
        if node.color == 'N':
            remaining = True
            break

    if remaining == False:
        return

    edges = currMap.getEdges(curr)

    unvisited = list()
    nextColors = list(colors)
    currNode = tree[str(curr)]
    origColor = currNode.color
    currNode.visitedNum += 1

    for point in edges:
        tempPoint = tree[str(point)]
        if (tempPoint.color in nextColors):
            nextColors.remove(tempPoint.color)
        if (len(nextColors) == 0):
            return -1
        if point in visited:
            continue
        unvisited.append(point)

    for color in nextColors:
        currNode.color = color
        tree[str(curr)] = currNode

        for point in unvisited:
            if (_ColorMap(currMap, point, tree, visited, colors) == -1):
                continue

    currNode.color = origColor
    tree[str(curr)] = currNode
    visited.remove(curr)

    return 0

if __name__ == "__main__":
    name = "map"
    # for i in range(0, 10):
    #   Map(8).printJSON(name + str(i) + '.json')


    timeTrace = dict()
    treeTrace = dict()
    for i in range(2, 14):
        initial = time.time()
        ret = ColorMap(Map(i, i))
        end = time.time()
        timeTrace[i] = end - initial
        treeTrace[i] = ret

    for i in range(2, 14):
        print "______________________"
        print "For " + str(i) + " n"
        print timeTrace[i]
        avgVisited = 0
        for point, node in treeTrace[i].iteritems():
            if point == 'avgEdges':
                continue
            print point,
            print node.visitedNum
            avgVisited += node.visitedNum

        print avgVisited/i
        print treeTrace[i]['avgEdges']

