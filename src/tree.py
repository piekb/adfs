# This file describes the Tree structure


# A Root has data (interpretation string), children,
# i: an index of the child it should visit in the backward move,
# a list of msats, and the number of msats in the list.
class Root(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.i = 0
        self.msats = {}
        self.num = 0

    def add_child(self, data):
        obj = Node(data, self)
        self.children.append(obj)


# A Node has everything a Root has, plus a parent node.
class Node(object):
    def __init__(self, data, parent):
        self.data = data
        self.i = 0
        self.children = []
        self.parent = parent
        self.msats = {}
        self.num = 0

    def add_child(self, data):
        obj = Node(data, self)
        self.children.append(obj)


# Recursive definition of Depth-first pre-order traversal
def traverse(n, i):
    print((i*'--'), i, n.data)
    for child in n.children:
        traverse(child, i+1)
