from dsets import DSet
import random
from Queue import Queue
import pdb

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
				temp = dict(connectedFrom=list(), connectedTo=(-1,-1))
				row.append(temp)
			self.__map.append(row)

		self.__dset = DSet(size * size)
		self.__size = size
		self.__segments = []
		self.generate()
		self.printMap()

	def generate(self):
		first = self.__getPoint()

		while (True):	
			second = self.__findClosestPoint(first)

			if not second == (0,0):
				self.printMap()
				self.__dset.union(first[1] * self.__size + first[0], second[1] * self.__size + second[0])

				self.__map[first[0]][first[1]]['connectedTo'] = second
				self.__map[second[0]][second[1]]['connectedFrom'].append(first)

				self.__segments.append((first, second))
				first = second
			else:
				break

	def printMap(self):
		for row in self.__map:
			for elem in row:
				print elem,
			print ""

		for segment in self.__segments:
			print str(segment[0]) + "->" + str(segment[1])

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

	def connected(self, coord, second):
		return (coord in self.__map[second[0]][second[1]]['connectedFrom'] or 
				second == self.__map[coord[0]][coord[1]]['connectedTo'] or
				coord == self.__map[second[0]][second[1]])

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

		for segment in self.__segments:
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
	Map(5)
