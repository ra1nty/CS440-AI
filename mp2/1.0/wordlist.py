import os
import sys
from trie import Trie

class wordList:

    wordlist_dir = "./wordlist/"
    sections = dict()
    words = dict()
    wordSubjectRelation = dict()

    def __init__(self):
        files = os.listdir(self.wordlist_dir)
        self.trie = Trie()

        for f in files:
            with open(self.wordlist_dir + f, 'r') as word_file:
                temp = word_file.read()

            lines = temp.replace('\r', '').split('\n')
            self.sections[f.replace('.txt', '')] = lines
            for line in lines:
                pass

        self.generateWordSubjectRel()
        self.fillTrie()


    def generateWordSubjectRel(self):
        for subject, words in self.words.itertools():
            for word in words:
                self.wordSubjectRelation[word] = subject

    def fillTrie(self):
        for word in self.wordSubjectRelation.keys():
            self.trie.insert(word)
        return self.trie

    def printWordList(self):
        for k, v in self.sections.iteritems():
            print k + ': ',
            print v

if __name__ == "__main__":
    wordList().printWordList()
