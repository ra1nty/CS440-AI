import os
import sys
from trie import Trie
from sets import Set

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

    def validAnswers(self, subject, word):
        answers = list()

        if subject in self.sections:
            words = self.sections[subject]
        else:
            return answers

        for w in words:
            match = 1
            for i in xrange(0, len(word)):
                if word[i] == " ":
                    continue

                if w[i] == word[i]:
                    continue
                else:
                    match = 0
                    break

            if match:
                answers.append(w)

        return answers


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

    def printWordList(self):
        for k, v in self.sections.iteritems():
            print k + ': ',
            print v

if __name__ == "__main__":
    wordList().autoCompleteSubject(["adverb", "noun"], "")
