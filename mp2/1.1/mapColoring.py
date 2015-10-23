from dsets import DSet
import random
from Queue import Queue
import pdb
import json

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
		self.generate()
		self.printMap()

	def generate(self):
		first = self.__getPoint()

		while (True):	
			second = self.__findClosestPoint(first)

			if not second == (0,0):
				self.__dset.union(first[1] * self.__size + first[0], second[1] * self.__size + second[0])

				self.__map[first[0]][first[1]]['connected'].append(second)
				self.__map[second[0]][second[1]]['connected'].append(first)

				self.__edges.append((first, second))
				first = second
			else:
				break

	def printMap(self):
		for row in self.__map:
			for elem in row:
				print elem,
			print ""

		for segment in self.__edges:
			print str(segment[0]) + "->" + str(segment[1])

		with open('map.json', 'w') as f:
			graph = list()
			output = {}

			output['size'] = self.__size
			for row in self.__map:
				for elem in row:
					graph.append(elem)
					
			output['graph'] = graph
			output['edges'] = self.makeEdgeList()

			f.write(json.dumps(output))

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

		while not nextPoint.empty():
			temp = nextPoint.get()

			if not temp == first:
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

		return (0,0)

	def connected(self, first, second):
		return (first in self.__map[second[0]][second[1]]['connected'] or
				second in self.__map[first[0]][first[1]]['connected'])

	def __getPoint(self):
		x = random.randint(0, self.__size - 1)
		y = random.randint(0, self.__size - 1)

		return (x, y)

	# From http://paulbourke.net/geometry/pointlineplane/
	def doesIntersect(self, start, end):
		startX = start[0]
		startY = start[1]

		endX = end[0]
		endY = end[1]

		for segment in self.__edges:
			segStart = segment[0]
			segEnd = segment[1]

			segStartX = segStart[0]
			segStartY = segStart[1]

			segEndX = segEnd[0]
			segEndY = segEnd[1]

			denom = (segEndY - segStartY)*(endX - startX) - (segEndX - segStartX)*(endY - startY)
			
			if denom == 0:
				return False

			Ua = ((segEndX - segStartX)*(startY - segStartY) - (segEndY - segStartY)*(startX - segStartX))/denom
			Ub = ((endX - startX)*(startY - segStartY) - (endY - startY)*(startX - segStartX))/denom
			
			Ua = abs(Ua)
			Ub = abs(Ub)

			if (Ua < 1 and Ua > 0) or (Ub < 1 and Ub > 0):
				return True

		return False


if __name__ == "__main__":
	Map(10)
