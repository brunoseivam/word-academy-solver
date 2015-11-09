# Trie implementation based on stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python

import math, time, sys
from collections import deque
import cPickle as pickle

class Trie:
    END='_end'

    def __init__(self, filename=None, pickled=False):
        self.root = dict()

        if filename:
            with open(filename) as db:
                if pickled:
                    self.root = pickle.load(db)
                else:
                    self.add([word.strip() for word in db])

    def add(self, words):
        for word in words:
            d = self.root
            for letter in word:
                d = d.setdefault(letter, {})
            d[self.END] = self.END

    def __contains__(self, key):
        return self.has(key)

    def has(self, word, prefix=False):
        d = self.root
        for letter in word:
            if letter in d:
                d = d[letter]
            else:
                return False
        return self.END in d or prefix

class Puzzle:
    EMPTY='.'

    def __init__(self, puzzle):
        size = len(puzzle)

        if int(math.sqrt(size) + 0.5)**2 != size:
            raise("Invalid non-square puzzle")

        self.side   = int(math.sqrt(size))
        self.puzzle = puzzle.lower()
        self.valid  = set(i for i, letter in enumerate(self.puzzle) if letter != self.EMPTY)
        self.path   = []
        self.recalcChoices()
        self.coord  = [(i/self.side,i%self.side) for i in xrange(size)]

    def __repr__(self):
        return "\n".join(self.puzzle[i:i+self.side] for i in range(0, self.side**2, self.side))

    def position(self, row, col):
        return row*self.side + col

    def distance(self, p1, p2):
        c1 = self.coord[p1]
        c2 = self.coord[p2]
        return max((abs(c1[0]-c2[0]),abs(c1[1]-c2[1])))

    def recalcChoices(self):
        if not self.path:
            self.choices = self.valid.copy()
        else:
            self.choices = [c for c in self.valid - set(self.path) if self.distance(self.path[-1], c)==1]

    def getPath(self):
        return ("".join(self.puzzle[i] for i in self.path), tuple(self.path), self.applyPath())

    def applyPath(self):
        # Create a new list of tiles, marking the ones in the path as empty
        puzzle = list(self.puzzle)
        for p in self.path:
            puzzle[p] = self.EMPTY

        # Mark all path tiles as invalid and convert to reverse sorted coordinates
        valid = [self.coord[p] for p in sorted(self.valid-set(self.path), reverse=True)]

        for row, col in valid:
            offset = sum((rowBelow,col) not in valid for rowBelow in xrange(row+1, self.side))
            oldPos = self.position(row, col)
            newPos = self.position(row+offset, col)
            puzzle[oldPos], puzzle[newPos] = puzzle[newPos], puzzle[oldPos]

        return Puzzle("".join(puzzle))

    def solve(self, trie, wordLen):
        self.solutions = []
        self.doSolve(trie, wordLen)
        return self.solutions

    def doSolve(self, trie, wordLen):
        for c in self.choices:
            self.path.append(c)
            self.recalcChoices()

            if trie.has(self.getPath()[0], wordLen > 1):
                if wordLen > 1:
                    self.doSolve(trie, wordLen-1)
                else:
                    self.solutions.append(self.getPath())

            self.path.pop()
            self.recalcChoices()

if __name__ == '__main__':
    puzzleString = sys.argv[1]
    wordLengths  = [int(a) for a in sys.argv[2:]]

    dbFile = 'db/db.txt'
    print "[DEBUG] Loading database", dbFile, "..."
    trie = Trie(dbFile)
    print "[DEBUG] Database loaded"

    pending = [( (), Puzzle(puzzleString))]
    for wl in wordLengths:
        newPending = []
        for solution, puzzle in pending:
            for s in puzzle.solve(trie, wl):
                newPending.append((solution+(s[0],), s[2]))
        pending = newPending

    for s in set(s[0] for s in pending):
         print s
