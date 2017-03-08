from PythonApplication1 import *

POSPATH = 'positives.txt'
NEGPATH = 'negatives.txt'

class trie():
    DEFAULT_ALPH = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','-','+']

    def __init__(self, a=DEFAULT_ALPH):
        self.alph = a
        self.root = node(self.alph, '', 0)

    def add(self, s, posneg):
        w = s + " "
        curr = self.root
        while(w != " "):
            c = w[0]
            w = w[1:]
            if not curr.hasChild(c):
                curr.addChild(c)
            curr = curr.getChild(c)
        if curr.hasWord() != None: raise Exception("Tree already has a the {} word ,\"{}\", assigned".format("positive" if curr.hasWord() else "negative", s))
        return curr.addWord(posneg)

    def search(self, s):
        w = s.lower() + " "
        curr = self.root
        while(w != " "):
            c = w[0]
            w = w[1:]
            curr = curr.getChild(c)
            if curr is None:
                return None
        return curr.hasWord()

    def getAllWords(self):
        list = []
        stack = []
        w = []
        stack.insert(0, self.root)
        while(len(stack) != 0):
            curr = stack.pop()
            if(curr.getDepth() <= len(w) - 1):
                w = w[:curr.getDepth()]
            w.append(curr.getKey())
            if curr.hasChildren():
                for d,node in curr.getChildren().items():
                    stack.append(node)
            if curr.hasWord() != None:
                list.append(''.join(w))
        return list

class node():
    def __init__(self, a, c, d):
        self.alph = a
        self.key = c
        self.depth = d
        self.children = dict()
        self.word = None
    
    def getKey(self):
        return self.key

    def getDepth(self):
        return self.depth

    def addChild(self, c):
        self.children[c] = node(self.alph, c, self.depth+1)
        return True

    def getChild(self, c):
        if self.hasChild(c):
            return self.children[c]
        else:
            return None

    def hasChild(self, c):
        return c in self.children

    def getChildren(self):
        return self.children

    def hasChildren(self):
        return len(self.children) != 0

    def addWord(self, posneg):
        self.word = posneg
        return True

    def hasWord(self):
        return self.word

class searchClass:
    def __init__(self):
        self.tree = trie()

    def addWords(self, path, posneg):
        with open(path, "r") as file:
            for line in file:
                self.tree.add(line[:-1], posneg)

    def addPositives(self, dir):
        path = dir + POSPATH
        self.addWords(path, True)

    def addNegatives(self, dir):
        path = dir + NEGPATH
        self.addWords(path, False)

def test(dir):
    t = searchClass()
    t.addPositives(dir)
    t.addNegatives(dir)
    list = ["cool", "zombie", "smojoho", "koalabear"]
    print("-------------")
    for s in t.tree.getAllWords(): print(s + ":" + str(t.tree.search(s)))
    print("-------------")
    for s in list: print(s +":"+ str(t.tree.search(s)))