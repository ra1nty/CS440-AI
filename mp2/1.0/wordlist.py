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
        self.trieFilled = False

    def generateWordSubjectRel(self):
        for subject, words in self.sections.iteritems():
            for word in words:
                if word in self.wordSubjectRelation.keys():
                    tempSubject = self.wordSubjectRelation[word]
                    tempSubjectList = list()
                    if type(tempSubject) is list:
                        for sub in tempSubject:
                            tempSubjectList.append(sub)
                    else:
                        tempSubjectList.append(tempSubject)
                    tempSubjectList.append(subject)
                    self.wordSubjectRelation[word] = tempSubjectList
                else:
                    self.wordSubjectRelation[word] = subject

    def getSubject(self, word):
        if word not in self.wordSubjectRelation.keys():
            return "None"
        else:
            return self.wordSubjectRelation[word]

    def getWordsBySubject(self, subject):
        return self.sections[subject]

    def getTrie(self):
        if not self.trieFilled:
            for word in self.wordSubjectRelation.keys():
                self.trie.insert(word)
            self.trieFilled = True
        return self.trie

    def printWordList(self):
        for k, v in self.sections.iteritems():
            print k + ': ',
            print v

if __name__ == "__main__":
    wordList().printWordList()
