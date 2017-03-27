import PythonApplication1 as main

POSPATH = 'positives'
NEGPATH = 'negatives'

DEFAULT_ALPH = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','\-','\+']

class trie():
    def __init__(self, a=DEFAULT_ALPH):
        self.alph = a
        self.root = node(self.alph, '', 0)

    def add(self, s, posneg):
        curr = self.root
        for c in s.lower():
            if not curr.hasChild(c):
                curr.addChild(c)
            curr = curr.getChild(c)
        if curr.hasWord() != None:
            raise Exception("Tree already has a the {} word ,\"{}\", assigned".format("positive" if curr.hasWord() else "negative", s))
        return curr.addWord(posneg)

    def search(self, s):
        curr = self.root
        for c in s.lower():
            curr = curr.getChild(c)
            if curr is None:
                return None
        return curr.hasWord()

    def getAllWords(self):
        list = []
        stack = []
        w = "$"
        stack.insert(0, self.root)
        while(len(stack) != 0):
            curr = stack.pop()
            if(curr.getDepth() <= len(w)-1):
                w = w[:curr.getDepth()]
            w = w + curr.getKey()
            if curr.hasChildren():
                for d,node in curr.getChildren().items():
                    stack.append(node)
            if curr.hasWord() != None:
                list.append(w[1:])
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

def addWords(t, path, posneg):
    with open(path, "r") as file:
        for line in file:
            t.add(line[:-1], posneg)

def addPositives(t):
    path = main.getDataPath(POSPATH)
    addWords(t, path, True)

def addNegatives(t):
    path = main.getDataPath(NEGPATH)
    addWords(t, path, False)

def getSearchTrie():
    t = trie()
    addPositives(t)
    addNegatives(t)
    
    return t