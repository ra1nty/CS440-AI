import os
import sys
import trie

class wordList:

    wordlist_dir = "./wordlist/"
    words = dict()
    wordSubjectRelation = dict()

    def __init__(self):
        files = os.listdir(self.wordlist_dir)

        for f in files:
            with open(self.wordlist_dir + f, 'r') as word_file:
                temp = word_file.read()

            lines = temp.replace('\r', '').split('\n')
            self.words[f.replace('.txt', '')] = lines

    def generateWordSubjectRel(self):

        for subject, words in self.words.itertools():
            for word in words:
                self.wordSubjectRelation[word] = subject

    def printWordList(self):
        for k, v in self.words.iteritems():
            print k + ': ',
            print v

if __name__ == "__main__":
    wordlist().printWordList()
