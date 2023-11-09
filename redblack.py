
# File:     red_black.py
# Author:   John Longley
# Date:     October 2023

# Template file for Inf2-IADS (2023-24) Coursework 1, Part B:
# Implementation of dictionaries by red-black trees, space-saving version.

# Provided code:

from enum import Enum

Colour = Enum('Colour', ['Red', 'Black'])
Red, Black = Colour.Red, Colour.Black


def colourStr(c):
    return 'R' if c == Red else 'B'


Dir = Enum('Dir', ['Left', 'Right'])
Left, Right = Dir.Left, Dir.Right


def opposite(d):
    if d == Left:
        return Right
    else:
        return Left


def branchLabel(d):
    if d == Left:
        return 'l'
    else:
        return 'r'


class Node():

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.colour = Red
        self.left = None
        self.right = None

    def getChild(self, branch):
        if branch == Left:
            return self.left
        else:
            return self.right

    def setChild(self, branch, y):
        if branch == Left:
            self.left = y
        else:
            self.right = y

    def __repr__(self):
        return str(self.key) + ':' + str(self.value) + ':' + colourStr(self.colour)

# Use None for all trivial leaf nodes


def colourOf(x):
    if x is None:
        return Black
    else:
        return x.colour


class RedBlackTree():

    def __init__(self):
        self.root = None
        self.stack = []


# TODO: Task 1.


    def lookup(self, key):
        # return value associated with key, or None if no such key
        # (this is a wrapper for the recursive method)
        return self.lookup_(self.root, key)

    def lookup_(self, x, key):
        # return value associated with key in subtree rooted at x,
        # or None if no such key
        if x == None:
            return None
        elif key == x.key:
            return x.value
        elif key < x.key:
            return self.lookup_(x.left, key)
        else:
            return self.lookup_(x.right, key)


# TODO: Task 2.


    def plainInsert(self, key, value):
        # insert key-value pair into tree
        # (this is a wrapper for the recursive method)
        if self.root == None:
            self.root = Node(key, value)
        else:
            self.plainInsert_(self.root, key, value)

    def plainInsert_(self, x, key, value):
        self.stack.append(x)  # Add x to the stack

        # If the key already exists, update the value
        if key == x.key:
            x.value = value

        # If the key is less than the current node's key, go left
        elif key < x.key:
            self.stack.append(Left)
            # If there is no left child, create a new node and add it as the left child
            if x.left == None:
                x.left = Node(key, value)
                self.stack.append(x.left)
            else:  # If there is a left child, recursively call plainInsert_ on it
                self.plainInsert_(x.left, key, value)

        else:
            self.stack.append(Right)
            # If there is no right child, create a new node and add it as the right child
            if x.right == None:
                x.right = Node(key, value)
                self.stack.append(x.right)
            else:  # If there is a right child, recursively call plainInsert_ on it
                self.plainInsert_(x.right, key, value)


# TODO: Task 3.


    def tryRedUncle(self):
        # If the stack is too short, return False
        if len(self.stack) < 5:
            return False

        # Get the parent, grandparent, and uncle
        me = self.stack[-1]
        parent = self.stack[-3]
        grandparent = self.stack[-5]
        uncle = grandparent.getChild(opposite(self.stack[-4]))

        # Check if red uncle case applies
        if colourOf(me) == Red and colourOf(parent) == Red and colourOf(uncle) == Red:
            # Flip the colours of the grandparent, parent, and uncle
            grandparent.colour = Red
            parent.colour = Black
            uncle.colour = Black

            # pop the three nodes from the stack
            for i in range(4):
                self.stack.pop()

            return True

        else:
            # If the red uncle case does not apply, return False
            return False

    def repeatRedUncle(self):
        while self.tryRedUncle():
            pass


# Provided code to support Task 4:

    def toNextBlackLevel(self, node):
        # inspect subtree down to the next level of blacks
        # and return list of components (subtrees or nodes) in L-to-R order
        # (in cases of interest there will be 7 components A,a,B,b,C,c,D).
        if colourOf(node.left) == Black:  # node.left may be None
            leftHalf = [node.left]
        else:
            leftHalf = self.toNextBlackLevel(node.left)
        if colourOf(node.right) == Black:
            rightHalf = [node.right]
        else:
            rightHalf = self.toNextBlackLevel(node.right)
        return leftHalf + [node] + rightHalf

    def balancedTree(self, comps):
        # build a new (balanced) subtree from list of 7 components
        [A, a, B, b, C, c, D] = comps
        a.colour = Red
        a.left = A
        a.right = B
        c.colour = Red
        c.left = C
        c.right = D
        b.colour = Black
        b.left = a
        b.right = c
        return b


# TODO: Task 4.

    def endgame(self):
        pass

    def insert(self, key, value):
        pass


# Provided code:

    # Printing tree contents

    def __str__(self, x):
        if x == None:
            return 'None:B'
        else:
            leftStr = '[ ' + self.__str__(x.left) + ' ] '
            rightStr = ' [ ' + self.__str__(x.right) + ' ]'
            return leftStr + x.__str__() + rightStr

    def __repr__(self):
        return self.__str__(self.root)

    def showStack(self):
        return [x.__str__() if isinstance(x, Node) else branchLabel(x)
                for x in self.stack]

    # All keys by left-to-right traversal

    def keysLtoR_(self, x):
        if x == None:
            return []
        else:
            return self.keysLtoR_(x.left) + [x.key] + self.keysLtoR_(x.right)

    def keysLtoR(self):
        return self.keysLtoR_(self.root)

# End of class RedBlackTree


# Creating a tree by hand:

sampleTree = RedBlackTree()
sampleTree.root = Node(2, 'two')
sampleTree.root.colour = Black
sampleTree.root.left = Node(1, 'one')
sampleTree.root.left.colour = Black
sampleTree.root.right = Node(4, 'four')
sampleTree.root.right.colour = Red
sampleTree.root.right.left = Node(3, 'three')
sampleTree.root.right.left.colour = Black
sampleTree.root.right.right = Node(6, 'six')
sampleTree.root.right.right.colour = Black


# For fun: sorting algorithm using trees
# Will remove duplicates (not good)

def treeSort(L):
    T = RedBlackTree()
    for x in L:
        T.insert(x, None)
    return T.keysLtoR()

# End of file
