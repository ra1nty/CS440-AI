import os
import sys

class wordList:

    wordlist_dir = "./wordlist/"
    words = dict()

    def __init__(self):
        files = os.listdir(self.wordlist_dir)

        for f in files:
            with open(self.wordlist_dir + f, 'r') as word_file:
                temp = word_file.read()

            lines = temp.replace('\r', '').split('\n')
            self.words[f.replace('.txt', '')] = lines

    def printWordList(self):
        for k, v in self.words.iteritems():
            print k + ': ',
            print v

if __name__ == "__main__":
    wordlist().printWordList()
