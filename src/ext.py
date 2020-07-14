import copy
from copy import deepcopy
import time

inters = []


# The main recursive method to print all possible interpretations
def allKLengthRec(set, prefix, n, k):
    # Base case: k is 0,
    # add to set
    if k == 0:
        inters.append(prefix)
        return

    # One by one add all characters from set
    # and recursively call for k equals to k-1
    for i in range(n):
        # Next character of input added
        newPrefix = prefix + set[i]

        # k is decreased, because
        # we have added a new character
        allKLengthRec(set, newPrefix, n, k - 1)


def gen_inters(size):
    allKLengthRec(['u', 't', 'f'], "", 3, size)
    return inters


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


def combine_msats(msats):
    global set_m, full
    full = []
    set_m = list(msats.values())
    combine_rec(0, [])

    new_m = {}
    i = 0
    for k in list(msats.keys()):
        x = []
        for n in full:
            x.append(n[i])
        new_m[k] = x
        i += 1

    return new_m


if __name__ == '__main__':
    y = combine_msats(m)
