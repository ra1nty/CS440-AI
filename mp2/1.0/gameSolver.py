import os
import sys
from sets import Set
from wordlist import wordList
from trie import Trie

class WordGame:

    properties = dict()
    wordList = wordList()

    class CSPNode:

        def __init__(self, game=list(), word="", subject=""):
            self.children = list()
            self.currGame = game
            self.currWord = word
            self.currSubject = subject
            self.solution = False

        def isLeaf(self):
            return len(self.children) == 0

        def isSolution(self):
            return self.solution

        def markSolution(self):
            self.solution = True

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
        self.__bruteForceLetterBased(self.root, [" "] * self.length, solutions, solutionSet)

        for solution in solutions:
            print solution

    def __bruteForceLetterBased(self, subroot, curr, solutions, solutionSet):
        if not curr[len(curr) - 1] == " ":
            if "".join(curr) not in solutionSet:
                solutionSet.add("".join(curr))
                solutions.append("".join(curr))
            return

        idx = 0
        for i in range(0, len(curr)):
            if curr[i] == " ":
                idx = i
                break

        sub = ""
        indicesActual = list()
        for subject, indices in self.properties.iteritems():
            for indice in indices:
                if indice == idx:
                    sub = subject
                    indicesActual = indices
                    break

        word = ""
        insertIdx = 0
        for i in range(0, len(indicesActual)):
            if indicesActual[i] == idx:
                insertIdx = i

            word += curr[indice]

        autoCompletes = self.wordList.autoCompleteSubject(sub, word)

        for autoComplete in autoCompletes:
            tempChar = autoComplete[insertIdx]
            tempCurr = list(curr)
            tempCurr[idx] = tempChar
            tempNode = self.CSPNode(tempCurr)
            subroot.children.append(tempNode)
            self.__bruteForceLetterBased(tempNode, tempCurr, solutions, solutionSet)

    def bruteForceWordBased(self):
        trie = wordList().getTrie()

        subject = self.properties.keys()
        idx = 0
        solutions = list()
        solutionSet = Set()

        self.__bruteForceWordBased(self.root, subject, [" "] * (self.length), solutions, solutionSet)

        for solution in solutions:
            if self.verifySolution(solution):
                print "".join(solution) + " is a valid solution!"
            else:
                print "".join(solution) + " is not a valid solution :("

    def __bruteForceWordBased(self, subroot, subjects, curr, solutions, solutionSet):
        if len(subjects) == 0:
            if "".join(curr) not in solutionSet:
                solutions.append(subroot.currGame)
                solutionSet.add("".join(curr))
            subroot.markSolution()
            return

        for subject in subjects:
            wordList = self.wordList.getWordsBySubject(subject)
            indices = self.properties[subject]

            temp_subjects = list(subjects)
            temp_subjects.remove(subject)
            for word in wordList:
                first = curr[int(indices[0])]
                second = curr[int(indices[1])]
                third = curr[int(indices[2])]

                if first != " ":
                    if first != word[0]:
                        continue
                if second != " ":
                    if second != word[1]:
                        continue
                if third != " ":
                    if third != word[2]:
                        continue

                temp_curr = list(curr)
                temp_curr[indices[0]] = word[0]
                temp_curr[indices[1]] = word[1]
                temp_curr[indices[2]] = word[2]
                temp_child = self.CSPNode(temp_curr, word, subject)

                self.__bruteForceWordBased(temp_child, temp_subjects, temp_curr, solutions, solutionSet)
                subroot.children.append(temp_child)
                continue

    def printWordGame(self):
        for k,v in self.properties.iteritems():
            print k + ':',
            print v

gameDirectory = './games/'

def main():
    argv = sys.argv

    game = WordGame(gameDirectory + argv[1] + '.game')
    game.printWordGame()
    game.bruteForceLetterBased()


if __name__ == "__main__":
    main()

