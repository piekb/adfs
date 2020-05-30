import json

deltas = ['tfu', 'ffu', 'ttt']

class Root(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.visited = False

    def add_child(self, data):
        obj = Node(data, self)
        self.children.append(obj)


class Node(object):
    def __init__(self, data, parent):
        self.data = data
        self.children = []
        self.visited = False
        self.parent = parent

    def add_child(self, data):
        obj = Node(data, self)
        self.children.append(obj)


def traverse(n, i):
    """Depth-first pre-order."""
    print(i, n.data)
    for child in n.children:
        traverse(child, i+1)


def test_tree():
    n = Root('uuu')
    for m in deltas:
        n.add_child(m)

    for c in n.children:
        print(c.data, c.parent.data)



if __name__ == '__main__':
    test_tree()

