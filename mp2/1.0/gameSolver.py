import os
import sys
from wordlist import wordList
from trie import Trie

class WordGame:

    lengthOfGame = 0
    properties = dict()
    wordList = wordList()

    def __init__(self, filename):
        with open(filename, 'r') as f:
            temp = f.read()

        # Parse the file and remove spaces and split by newline
        lines = temp.replace('\r', '').replace(' ', '').split('\n')
        length = int(lines.pop(0))
        self.lengthOfGame = length

        for line in lines:
            lineTokens = line.split(':')
            if len(lineTokens) == 2:
                self.properties[lineTokens[0]] = lineTokens[1].split(',')

    def bruteForce(self):

        pass

    def printWordGame(self):
        for k,v in self.properties.iteritems():
            print k + ':',
            print v

gameDirectory = './games/'

def main():
    argv = sys.argv

    game = WordGame(gameDirectory + argv[1] + '.game')


if __name__ == "__main__":
    main()

