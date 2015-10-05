import os
import sys

class Trie:

    class TrieNode:

        def __init__(self, currLetter=-1):
            # Children will be populated at runtime, better for space
            self.children = dict()
            self.letter = currLetter
            self.isRoot = False
            self.isWord = False

    def __init__(self):
        self.root = self.TrieNode()
        self.root.isRoot = True
        self.size = 0

    def insert(self, word=""):
        if not word == "":
            word = word.lower()
            self.__insert(self.root, word, 0)

    def __insert(self, subroot, word, idx):
        if len(word) - 1 is idx:
            subroot.children[word[idx]] = self.TrieNode(word[idx])
            subroot.children[word[idx]].isWord = True
        else:
            if word[idx] not in subroot.children.keys():
                subroot.children[word[idx]] = self.TrieNode(word[idx])
            self.__insert(subroot.children[word[idx]], word, idx+1)

    def search(self, word=""):
        if not word == "":
            word = word.lower()
            return self.__search(self.root, word, 0)

    def __search(self, subroot, word, idx):
        if len(word) - 1 is idx:
            if word[idx] in subroot.children.keys():
                return subroot.children[word[idx]].isWord
            else:
                return False
        else:
            if word[idx] not in subroot.children.keys():
                return False
            else:
                return self.__search(subroot.children[word[idx]], word, idx + 1)



def testTrie():
    trie = Trie()

    testWords = ["AlphA", "abrar", "HypOPoMous", "test", "testtt"]
    verifyWords = ["alpHa", "aBrar", "HypoPoMous", "Test", "testt"]

    for word in testWords:
        trie.insert(word)

    for idx in range(0, len(testWords)):
        if trie.search(verifyWords[idx]):
            print "Passes test %s is found!" % (verifyWords[idx])
        else:
            print "Passes test %s is not found!" % (verifyWords[idx])


if __name__ == "__main__":
    testTrie()
