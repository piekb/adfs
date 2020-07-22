import copy
from copy import deepcopy

inters = []


# Recursive method to generate all possible interpretations
def gen_rec(set, prefix, n, k):
    # Base case
    if k == 0:
        inters.append(prefix)
        return

    # One by one add all characters from set and recursively call for k equals to k-1
    for i in range(n):
        # Next character of input added
        newPrefix = prefix + set[i]

        # k is decreased, because we have added a new character
        gen_rec(set, newPrefix, n, k - 1)


# Generate all interpretations of a certain size.
def gen_inters(size):
    gen_rec(['u', 't', 'f'], "", 3, size)
    return inters


# Combine mSATs such that each set has the same length,
# and contains one mSAT per argument in A'.
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
