import copy
from copy import deepcopy

inters = []


# The main recursive method to print all possible interpretations
def allKLengthRec(set, prefix, n, k):
    # Base case: k is 0,
    # add to set
    if k == 0:
        inters.append(prefix)
        return

    # One by one add all characters
    # from set and recursively
    # call for k equals to k-1
    for i in range(n):
        # Next character of input added
        newPrefix = prefix + set[i]

        # k is decreased, because
        # we have added a new character
        allKLengthRec(set, newPrefix, n, k - 1)


def gen_inters(size):
    # inters = []
    allKLengthRec(['u', 't', 'f'], "", 3, size - 1)
    return inters


# Trees:
#   http://en.wikipedia.org/wiki/Tree_(data_structure)
#   http://en.wikipedia.org/wiki/Tree_traversal


class Tree(object):
    """Generic tree."""

    def __init__(self, name='', children=None):
        self.name = name
        if children is None:
            children = []
        self.children = children

    def __str__(self):
        return str(self.name)


def walk_tree_df_preorder(node, visit):
    """Depth-first pre-order."""
    visit(node)
    for child in node.children:
        walk_tree_df_preorder(child, visit)


def walk_tree_df_postorder(node, visit):
    """Depth-first post-order."""
    for child in node.children:
        walk_tree_df_preorder(child, visit)
    visit(node)


def test_tree():
    T = Tree

    def visit(n):
        print(n)

    #    *
    #   / \
    #  1   +
    #     / \
    #    2   -
    #       / \
    #      3   4
    t = T('1 if', [T('1.1 cond', [T('1.1.1 equal', [T('1.1.1.1 x'), T('1.1.1.2 y')])]),
                   T('1.2 true', [T('1.2.1 print', [T('1.2.1.1 OK')])]),
                   T('1.3 false', [T('1.3.1 end')])])
    print('=>Tree, Depth-First, Pre-Order')
    walk_tree_df_preorder(t, visit)
    print('=>Tree, Depth-First, Post-Order')
    walk_tree_df_postorder(t, visit)


m = {'a': ['1.1 tfu'], 'b': ['2.1 tuf', '2.2 ttt', '2.3 fff'], 'c': ['3.1 ftt', '3.2 tfu']}
set_m = list(m.values())

m_all = [['tfu', 'tuf', 'ftt'],
         ['tfu', 'ttt', 'ftt'],
         ['tfu', 'fff', 'ftt'],
         ['tfu', 'tuf', 'tfu'],
         ['tfu', 'ttt', 'tfu'],
         ['tfu', 'fff', 'tfu']]
full = []


def combine_rec(i, x):
    if i == len(set_m):
        y = deepcopy(x)
        full.append(y)
    else:
        for m in set_m[i]:
            x.append(m)
            combine_rec(i + 1, x)
            x.pop()


def combine():
    x = []
    for e in m['a']:
        print(f"{e} in m_a")
        x.append(e)
        for f in m['b']:
            print(f"{f} in m_b")
            x.append(f)
            for g in m['c']:
                print(f"{g} in m_c")
                x.append(g)
                # print(x)
                y = deepcopy(x)
                full.append(y)
                x.pop()
            x.pop()
        x.pop()

    # print(full)


def combine_msats(msats):
    # print("combining")
    # print(list(msats.keys()))
    # print(list(msats.values()))
    global set_m, full
    full = []
    set_m = list(msats.values())
    combine_rec(0, [])

    new_m = {}
    # print('hello', full)
    i = 0
    for k in list(msats.keys()):
        x = []
        for n in full:
            x.append(n[i])
            # print(n)
        new_m[k] = x
        # print(k, i)
        i += 1

    # print("hey", full)
    # print("ho", new_m)
    return new_m


if __name__ == '__main__':
    y = combine_msats(m)
#     print(y)
#     print(y['b'][4])
