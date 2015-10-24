import os
import sys
from sets import Set
from wordlist import wordList
from trie import Trie
from Queue import PriorityQueue, Queue
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

    class Indice:

        def __init__(self, indice, collisions, subjects):
            self.indice = indice
            self.collisions = collisions
            self.subjects = subjects

        def __cmp__(self, other):
            return self.indice < other.indice

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

    def letterBasedSolution(self):
        order = PriorityQueue()
        prevIndices = list()

        for i in xrange(0, self.length):
            collisions = 0
            subjects = list()

            for subject, indices in self.properties.iteritems():
                if i in indices:
                    idx = 0

                    collisions += 1
                    for indice in indices:
                        if i == indice:
                            break
                        idx += 1
                    subjects.append((subject, idx))

            newIndice = self.Indice(i, collisions, subjects)
            order.put(newIndice)

        stack = [] * order.qsize()
        while not order.empty():
            temp = order.get()
            stack.append(temp)
            print str(temp.indice) + " with " + str(temp.collisions) + " collisions"
            print temp.subjects

        solutionSet = Set()
        tree = self.CSPNode()
        currGame = [" "] * self.length
        self.__letterBasedSolution(tree, stack, currGame, solutionSet)

        for solution in solutionSet:
            print solution

        self.treeTrace(tree, 0, self.__printLetterSpaces);

    def __letterBasedSolution(self, subroot, order, curr, solutionSet):
        if len(order) == 0:
            for subject, indices in self.properties.iteritems():
                words = self.wordList.getWordsBySubject(subject)
                resultingWord = ""

                for indice in indices:
                    resultingWord += curr[indice]

                if not resultingWord in words:
                    return

            solutionSet.add("".join(curr))
            self.propogateSolution(subroot)
            return

        indice = order.pop() # Get the indice to fill in
        candidates = PriorityQueue()
        wordSet = Set()

        if len(order) > 0:
            nextIndice = order.pop()
            order.append(nextIndice)
        else:
            nextIndice = None

        letterSet = Set()
        for subjectTuple in indice.subjects:
            resultingWord = ""
            tempCurr = list(curr)
            subject = subjectTuple[0]
            wordIdx = subjectTuple[1]

            subjectIndices = self.properties[subject]

            for i in subjectIndices:
                resultingWord += curr[i]

            tempAnswers = self.wordList.validAnswers(subject, resultingWord)

            # Failed since there are no more valid answers
            if len(tempAnswers) == 0:
                order.append(indice)
                return

            for answer in tempAnswers:
                letterSet.add(answer[wordIdx])

        # pdb.set_trace()
        for letter in letterSet:
            tempCurr = list(curr)
            tempCurr[indice.indice] = letter

            if nextIndice is not None:
                mergeList = list()
                mergeSet = Set()

                for sub in nextIndice.subjects:
                    resultingWord = ""
                    subjectIndices = self.properties[sub[0]]
                    for i in subjectIndices:
                        resultingWord += tempCurr[i]

                    nextLevel = self.wordList.validAnswers(sub[0], resultingWord)

                    if len(nextLevel) == 0:
                        mergeList = list()
                        break

                    for next in nextLevel:
                        mergeSet.add(next)

                for next in mergeSet:
                    mergeList.append(next)

                candidates.put(self.Candidate(letter, len(mergeList), tempCurr))
            else:
                candidates.put(self.Candidate(letter, 0, tempCurr))

        while not candidates.empty():
            candidate = candidates.get()
            tempCurr = candidate.board
            newNode = self.CSPNode(game=tempCurr, word=candidate.name, parent=subroot)
            subroot.children.append(newNode)
            self.__letterBasedSolution(newNode, order, tempCurr, solutionSet)

        order.append(indice)

    def wordBasedSolution(self):
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
                        
            collisions = collisions * 20 - len(self.wordList.getWordsBySubject(checkerSubject))
            newSubject = self.Subject(checkerSubject, collisions)
            order.put(newSubject)
            tempOrder.put(newSubject)

        stack = [] * order.qsize()
        print "search order:",
        while not tempOrder.empty():
            temp = tempOrder.get()
            stack.append(temp)
            # print temp.name + " with " + str(temp.collisions) + " collisions"
            print temp.name + "->",

        print ""

        solutionSet = Set()
        tree = self.CSPNode()
        currGame = [" "] * self.length
        self.__wordBasedSolution(tree, stack, currGame, solutionSet)
#
#        for solution in solutionSet:
#            print solution

        print "root ->",
        self.treeTrace(tree, 0, self.__printSpaces)

    def __printSpaces(self, depth):
        for i in xrange(0, int(7 + 3.5*float(depth))):
            print " ",

    def __printLetterSpaces(self, depth):
        for i in xrange(0, int(5 + 2.5*float(depth))):
            print " ",

    def treeTrace(self, subroot, level, printspaces):
        if not subroot.solution:
            print "backtrace"
            return
        else:
            if len(subroot.children) == 0:
                print "(found result " + "".join(subroot.currGame) + ")"
            else:
                for child in subroot.children:
                    print child.currWord.strip(" ") + " ->",
                    self.treeTrace(child, level + 1, printspaces)
                    printspaces(level - 1)

            print ""

    def propogateSolution(self, subroot):
        while not subroot == None:
            subroot.markSolution()
            subroot = subroot.parent

    def __wordBasedSolution(self, subroot, order, curr, solutionSet):
        if len(order) == 0:
            solutionSet.add("".join(curr))
            self.propogateSolution(subroot)
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
            self.__wordBasedSolution(newNode, order, tempCurr, solutionSet)
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
    game.wordBasedSolution()
    game.letterBasedSolution()


if __name__ == "__main__":
    main()

