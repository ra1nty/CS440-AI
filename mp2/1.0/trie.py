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
            subroot.children[word[idx]] = TrieNode(word[idx])
            subroot.children[word[idx]].isWord = True
        else:
            try:
                subroot.children[word[idx]]
            except KeyError:
                subroot.children[word[idx]] = TrieNode(word[idx])
            finally:
                self.__insert(subroot.children[word[idx]], word, idx+1)

    def search(self, word=""):
        if not word == "":
            word = word.lower()
            self.__search(self.root, word, 0)

    def __search(self, subroot, word, idx):
        if len(word) - 1 is idx and subroot is not None:
            return subroot.isWord
        else:
            self.__search(subroot.children[word[idx]], word, idx + 1)


def testTrie():
    trie = Trie()

    testWords = ["Alpha", "abrar", "HypOPoMous"]
    verifyWords = ["alpHa", "aBrar", "HypoPoMous"]

    for word in testWords:
        trie.insert(word)

    for idx in range(0, len(testWords)):
        if testWords[idx] == verifyWords[idx]:
            if trie.search(verifyWords[idx]):
                print "Passes test %s is found!" % (verifyWords[idx])

        elif not testWords[idx] == verifyWords[idx]:
            if not trie.search(verifyWords[idx]):
                print "Passes test %s is not found!" % (verifyWords[idx])

if __name__ == "__main__":
    testTrie()
