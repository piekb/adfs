inters = []


# The main recursive method to print all possible interpretations
def allKLengthRec(set, prefix, n, k):
    # Base case: k is 0,
    # add to set
    if (k == 0):
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
    allKLengthRec(['u', 't', 'f'], "", 3, size - 1)
    return inters


# Trees:
#   http://en.wikipedia.org/wiki/Tree_(data_structure)
#   http://en.wikipedia.org/wiki/Tree_traversal
#   http://en.wikipedia.org/wiki/Binary_tree


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


if __name__ == '__main__':
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
