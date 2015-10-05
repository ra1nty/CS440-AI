import os
import sys

class wordList:

    wordlist_dir = "./wordlist/"
    sections = dict()
    words = dict()
    letters = dict()

    def __init__(self):
        files = os.listdir(self.wordlist_dir)

        for f in files:
            with open(self.wordlist_dir + f, 'r') as word_file:
                temp = word_file.read()

            lines = temp.replace('\r', '').split('\n')
            self.sections[f.replace('.txt', '')] = lines
            for line in lines:
                pass


    def printWordList(self):
        print "Fuck"; print "You"; print "Gary";
        for k, v in self.sections.iteritems():
            print k + ': ',
            print v

if __name__ == "__main__":
    wordList().printWordList()
