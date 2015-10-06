import os
import sys
from wordlist import wordList
from trie import Trie

class WordGame:

    properties = dict()
    wordList = wordList()

    def __init__(self, filename):
        with open(filename, 'r') as f:
            temp = f.read()

        # Parse the file and remove spaces and split by newline
        lines = temp.replace('\r', '').replace(' ', '').split('\n')
        length = int(lines.pop(0))

        for line in lines:
            lineTokens = line.split(':')
            if len(lineTokens) == 2:
                self.properties[lineTokens[0]] = lineTokens[1].split(',')

        self.string = [" "] * (length + 1)

    def verifySolution(self, trie, solution):
        for prop, indices in self.properties.iteritems():
            tempstr = str()
            for indice in indices:
                tempstr += solution[int(indice)]

            if self.wordList.getSubject(tempstr.upper()) == prop:
                continue

    def bruteForceWordBased(self):
        trie = wordList().getTrie()

        subject = self.properties.keys()
        idx = 0
        solutions = list()
        self.__bruteForceWordBased(trie, subject, idx, solutions)
        for solution in solutions:
            if self.verifySolution(trie, solution):
                print "".join(solution) + " is a valid solution!"
            else:
                print "".join(solution) + " is not a valid solution :("

    def __bruteForceWordBased(self, trie, subject, idx, solutions):
        if len(subject) == idx:
            temp = list(self.string)
            temp.pop(0)
            "".join(temp)
            solutions.append(temp)
            return

        indices = self.properties[subject[idx]]

        # These are the first, second, and third matches
        first = self.string[int(indices[0])]
        second = self.string[int(indices[1])]
        third = self.string[int(indices[2])]

        for word in self.wordList.getWordsBySubject(subject[idx]):
            if not first == " ":
                if not first == word[0]:
                    continue
            elif not second == " ":
                if not second == word[1]:
                    continue
            elif not third == " ":
                if not third == word[2]:
                    continue
            self.string[int(indices[0])] = word[0]
            self.string[int(indices[1])] = word[1]
            self.string[int(indices[2])] = word[2]
            self.__bruteForceWordBased(trie, subject, idx + 1, solutions)

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

