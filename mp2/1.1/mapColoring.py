__author__ = "Jeffrey Huang"

from DSet import DSet

def abs(num):
	if num < 0:
		return -num
	else:
		return num

class Map:

	def __init__(self, size):
		self.__map = [[] * size] * size
		self.__dset = DSet(size * size)
		self.__size = size
		self.__segments = []
		self.generate()

	def generate(self):
		joined = True

		while (joined):
			joined = False

			point = self.__getPoint()
			

	def __getPoint(self):
		x = random.randint(0, size)
		y = random.randint(0, size)

		return (x, y)

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

			Ua = ((segEndX - segStartX)*(startY - segStartY) - (segEndY - segStartY)*(startX - segStartX))/((segEndY - segStartY)*(endX - startX) - (segEndX - segStartX)*(endY - startY))
			Ub = ((endX - startX)*(startY - segStartY) - (endY - startY)*(startX - segStartX))/((segEndY - segStartY)*(endX - startX) - (segEndX - segStartX)*(endY - startY))
			
			Ua = abs(Ua)
			Ub = abs(Ub)

			if (Ua < 1 and Ua > 0) or (Ub < 1 and Ub > 0):
				return True

		return False
