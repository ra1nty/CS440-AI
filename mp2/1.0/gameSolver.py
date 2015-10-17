import os
import sys
from sets import Set
from wordlist import wordList
from trie import Trie
from Queue import PriorityQueue
import pdb

class WordGame:

    properties = dict()
    wordList = wordList()

    class CSPNode:

        def __init__(self, game=list(), word="", subject="", parent=None):
            self.children = list()
            self.currGame = game
            self.currWord = word
            self.currSubject = subject
            self.solution = False
            self.parent = parent

        def isLeaf(self):
            return len(self.children) == 0

        def isSolution(self):
            return self.solution

        def markSolution(self):
            self.solution = True

    class Candidate:

        def __init__(self, name, validAnswers, resultingBoard):
            self.name = name
            self.heuristic = validAnswers
            self.board = resultingBoard

        def __cmp__(self, other):
            return self.heuristic < other.heuristic

    class Subject:

        def __init__(self, name, collisions):
            self.name = name
            self.collisions = collisions

        def __cmp__(self, other):
            return self.collisions > other.collisions

    def __init__(self, filename):
        with open(filename, 'r') as f:
            temp = f.read()

        # Parse the file and remove spaces and split by newline
        lines = temp.replace('\r', '').replace(' ', '').split('\n')
        length = int(lines.pop(0))
        self.length = length

        for line in lines:
            lineTokens = line.split(':')
            if len(lineTokens) == 2:
                self.properties[lineTokens[0]] = list()
                for indice in lineTokens[1].split(','):
                    self.properties[lineTokens[0]].append(int(indice) - 1)

        self.string = [" "] * (length)
        self.length = length
        self.root = self.CSPNode()

    def verifySolution(self, solution):
        for prop, indices in self.properties.iteritems():
            tempstr = str()
            for indice in indices:
                tempstr += solution[indice]

            if self.wordList.getSubject(tempstr.upper()) == prop or prop in self.wordList.getSubject(tempstr.upper()):
                continue
            else:
                return False

        return True

    def bruteForceLetterBased(self):
        trie = wordList().getTrie()

        subject = self.properties.keys()
        solutions = list()
        solutionSet = Set()
        self.__bruteForceLetterBased(self.root, [" "] * self.length, 0, solutions, solutionSet)

        for solution in solutions:
            print solution

    def __bruteForceLetterBased(self, subroot, curr, idx, solutions, solutionSet):
        if idx == len(curr) - 1:
            if "".join(curr) not in solutionSet:
                solutionSet.add("".join(curr))
                solutions.append("".join(curr))
            return

        newCurr = list(curr)
        currIndices = []
        currSubject = list()

        for subject, indices in self.properties.iteritems():
            if idx in indices:
                currSubject.append(subject)
                currIndices = indices

        word = ""
        insertIdx = 0
        for i in range(0, len(indicesActual)):
            if indicesActual[i] == idx:
                insertIdx = i
        wordIdx = 0
        for indice in currIndices:
            if indice is idx:
                break
            wordIdx += 1

        candidates = self.wordList.autoCompleteSubjectLetter(currSubject, "".join(curr), wordIdx)
        print curr

        for candidate in candidates:
            newCurr[idx] = candidate
            print newCurr
            newNode = self.CSPNode(newCurr)
            subroot.children.append(newNode)
            self.__bruteForceLetterBased(newNode, newCurr, idx + 1, solutions, solutionSet)

    def bruteForceWordBased(self):
        order = PriorityQueue()
        tempOrder = PriorityQueue(order)

        for checkerSubject, checkerIndices in self.properties.iteritems():
            collisions = 0
            for subject, indices in self.properties.iteritems():
                if checkerSubject == subject:
                    continue

                for indice in checkerIndices:
                    if indice in indices:
                        collisions += 1

            newSubject = self.Subject(checkerSubject, collisions)
            order.put(newSubject)
            tempOrder.put(newSubject)

        stack = [] * order.qsize()
        while not tempOrder.empty():
            temp = tempOrder.get()
            stack.append(temp)
            print temp.name + " with " + str(temp.collisions) + " collisions"

        solutionSet = Set()
        tree = self.CSPNode()
        currGame = [" "] * self.length
        self.__bruteForceWordBased(tree, stack, currGame, solutionSet)

        for solution in solutionSet:
            print solution

    def __printSpaces(self, depth):
        for i in xrange(0, 4 + 7*depth):
            print " ",

    def __treeTrace(self, subroot, search, node):
        pass

    def __bruteForceWordBased(self, subroot, order, curr, solutionSet):
        if len(order) == 0:
            solutionSet.add("".join(curr))
            return

        # pdb.set_trace()
        subject = order.pop()
        indices = self.properties[subject.name]
        resultingWord = ""

        for indice in indices:
            resultingWord += curr[indice]

        words = self.wordList.validAnswers(subject.name, resultingWord)
        candidates = PriorityQueue()

        if not len(order) == 0:
            nextSubject = order.pop()
        else:
            nextSubject = None

        if nextSubject is not None:
            order.append(nextSubject)
            nextIndices = self.properties[nextSubject.name]

        for word in words:
            tempCurr = list(curr)
            i = 0

            for indice in indices:
                tempCurr[indice] = word[i]
                i += 1

            if nextSubject is not None:
                resultingWord = ""
                for indice in nextIndices:
                    resultingWord += tempCurr[indice]

                answers = self.wordList.validAnswers(nextSubject.name, resultingWord)
                candidates.put(self.Candidate(word, len(answers), tempCurr))
            else:
                candidates.put(self.Candidate(word, 0, tempCurr))

        # print "Order qsize: " + str(len(order))
        # print "Num candidates: " + str(candidates.qsize())

        while not candidates.empty():
            candidate = candidates.get()
            tempCurr = candidate.board
            newNode = self.CSPNode(tempCurr, candidate.name, subject, subroot)
            self.__bruteForceWordBased(newNode, order, tempCurr, solutionSet)
            subroot.children.append(newNode)

        order.append(subject)

    def printWordGame(self):
        for k,v in self.properties.iteritems():
            print k + ':',
            print v

gameDirectory = './games/'

def main():
    argv = sys.argv

    game = WordGame(gameDirectory + argv[1] + '.game')
    game.printWordGame()
    game.bruteForceWordBased()


if __name__ == "__main__":
    main()

