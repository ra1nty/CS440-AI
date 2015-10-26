from dsets import DSet
import random
from Queue import Queue
import pdb
import json
from sets import Set
import pprint
import png
import Image

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

	def generate(self):
		first = self.__getPoint()
		n = 25
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
	for i in range(0, 10):
		Map(7).printJSON("map" + str(i) + ".json")
