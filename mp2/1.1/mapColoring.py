from dsets import DSet
import random
from Queue import Queue
import pdb
import json
from sets import Set
import pprint

def abs(num):
	if num < 0:
		return -1 * num
	else:
		return num

class Map:

	def __init__(self, size):
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
		self.generate()
		self.__edgeList = self.makeEdgeList()

	def getInitialPoint():
		return self.__first

	def getEdges(self, point):
		return self.__edgeList[str(point)]

	def generate(self):
		self.__first = first = self.__getPoint()
		self.n = n = 30
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

	def printMap(self, name):
		for row in self.__map:
			for elem in row:
				print elem,
			print ""

		for segment in self.__edges:
			print str(segment[0]) + "->" + str(segment[1])

		with open(name, 'w') as f:
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
	_ColorMap(currMap=randomMap, curr=initialPoint, tree=nodeTree, visited=visited, colors=colors)
	pass

class colorNode:

	def __init__(self, color, point, edges):
		self.color = color
		self.point = point
		self.edges = edges

def _ColorMap(currMap=randomMap, curr=currPoint, tree=nodeTree, visited=visitedSet, colors=setOfColors):
	edges = randomMap.getEdges(currPoint)

	unvisited = list()
	for edge in edges:
		if edge in visitedSet:
			continue
		unvisited.append(edge)

	for edge in unvisited:
		edges = randomMap.getEdges(edge)

	pass

if __name__ == "__main__":
	name = "map"
	for i in range(0, 10):
		Map(8).printMap(name + str(i) + '.json')

	ColorMap(Map(8))
