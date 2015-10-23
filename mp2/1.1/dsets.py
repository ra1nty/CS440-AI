class DSet:

	def __init__(self, size):
		self.__elems = [-1] * size
		self.__size = size

	def union(self, root1, root2):

		if not (self.isSameSet(root1, root2)):
			if (self.__elems[root1] > -1):
				root1 = self.find(root1)
			if (self.__elems[root2] > -1):
				root2 = self.find(root2)

			newSize = self.__elems[root1] + self.__elems[root2]

			if (self.__elems[root1] <= self.__elems[root2]):
				self.__elems[root2] = root1
				self.__elems[root1] = newSize
			else:
				self.__elems[root1] = root2
				self.__elems[root2] = newSize

	def isSameSet(self, root1, root2):
		return self.find(root1) == self.find(root2)

	def freeNode(self, root):
		return self.__elems[root] == -1

	def find(self, root):
		if (self.__elems[root] >= 0):
			tempElem = self.find(self.__elems[root])
			self.__elems[root] = tempElem
			return tempElem

		return root

	def addElements(self, elems):
		for i in range(0, elems):
			self.__elems.append(-1)

if __name__ == "__main__":
	testDSets()