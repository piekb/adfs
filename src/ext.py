inters = []

# The main recursive method to print all possible interpretations
def allKLengthRec(set, prefix, n, k):

    # Base case: k is 0,
    # add to set
    if (k == 0) :
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
    allKLengthRec(['u', 't', 'f'], "", 3, size-1)
    return inters
