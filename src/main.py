# !/usr/bin/python3

import sys
import os
import sympy
import time
import random
import myfun
import forward
import tree
import msat_fun

from sympy import *
from myfun import *
from forward import *
from tree import *
from msat_fun import *


# An Argument has a name, acceptance condition, index, and SymPy symbol version of the name
class Argument:
    name = ""
    ac = ""
    sym = 0
    dex = 0


def xprint(string):
    if myfun.pc:
        print(string)


# Parses acceptance condition strings to find logical expressions and symbols
def rewrite(ac):
    iff = ac.replace('iff', 'Equivalent').replace('imp', 'Implies').replace('neg', 'Not')
    tf = iff.replace('and', 'And').replace('or', 'Or').replace('c(v)', 'True').replace('c(f)', 'False')

    # There might be a better way to convert a string to a formula, but for now this works.
    return simplify(tf)


def main():
    xprint("Hello!")

    # Get current working directory and append exercise input file to it
    cur_path = os.getcwd()
    part = os.path.split(cur_path)[0]

    # Get input file name and input file
    user_in = sys.argv[1]
    path = part + '/ex/' + user_in

    # Initialize internal representation of ADF and its size
    myfun.size = 0
    myfun.arguments = []

    # Read input file
    with open(path, 'r') as c:
        contents = c.readlines()
        for line in contents:
            if line[0] == 's':
                a = Argument()
                a.name = line[2:len(line)-3]
                a.sym = sympy.symbols(f"{a.name}")
                a.dex = myfun.size

                myfun.size += 1
                myfun.arguments.append(a)
            elif line[0:2] == 'ac':
                for a in myfun.arguments:
                    if a.name == line[3:line.find(',')]:
                        a.ac = rewrite(line[line.find(',')+1:(len(line) - 3)])
            else:
                print("Something's wrong with your input file.")

    if myfun.pc:
        print('Arguments in ADF:')
        myfun.print_full_args(myfun.arguments)
        print("-------------------")

    # Read initial claim and choice of algorithm from command line
    initial_claim = myfun.make_one(sys.argv[3], sys.argv[2])
    alg = int(sys.argv[4])
    xprint(f"v_0 = {initial_claim}")

    # Start game
    a_prime = myfun.check_info(initial_claim, myfun.size*'u')[0]
    n = tree.Root(initial_claim)
    k = 0  # depth
    winner = ''

    # Get one set of minimal satisfiable interpretations (one for each a in A')
    def get_m():
        n.num, n.msats = msat_fun.find_new(n.data, a_prime, alg)
        i = random.choice(range(n.num))
        forward.msat = {}
        for a in a_prime:
            forward.msat[f'{a.name}'] = n.msats[f'{a.name}'][i]
            n.msats[f'{a.name}'].remove(forward.msat[f'{a.name}'])
        n.num -= 1
    get_m()

    # Get delta(v_0, mSAT_A') and put it as the first child node
    update = forward.forward_step(initial_claim, a_prime)
    n.add_child(update)
    n = n.children[0]
    k += 1

    # Play the discussion game
    while True:
        xprint(f"v_{k} = {n.data}")
        a_prime, contra, found = myfun.check_info(n.data, n.parent.data)
        if contra:
            # Check if the current node represents the initial claim
            if type(n.parent) is tree.Root:
                xprint("Initial claim already gives a contradiction, P loses game")
                break

            # Apply the backward move
            xprint("Contradiction found, will apply backward move")
            found_msat = False

            # Loop until either a new mSAT is found, or we've backtracked to the initial claim
            while not found_msat and type(n) is not tree.Root:
                n = n.parent
                k -= 1
                xprint(f"\t Backtracked to v_{k} = {n.data}")

                # v_u = {u} is not in the tree, so v_0.parent does not exist
                if type(n) is tree.Root:
                    par = len(n.data) * 'u'
                else:
                    par = n.parent.data

                a_prime = myfun.check_info(v=n.data, oldv=par)[0]

                # Try to an unused mSAT, if the list is empty they've all been used
                if n.msats[f'{a_prime[0].name}']:
                    i = random.choice(range(n.num))
                    try_msat = {}
                    for a in a_prime:
                        try_msat[f'{a.name}'] = n.msats[f'{a.name}'][i]
                        n.msats[f'{a.name}'].remove(try_msat[f'{a.name}'])
                    n.num -= 1

                    found_msat = True

            if not found_msat:
                # We've backtracked to initial claim without finding an unused mSAT
                xprint("P loses game")
                break
            else:
                # Another mSAT is found, use it for the forward move and go to the new node
                xprint("\t Found another msat!")
                n.i += 1
                forward.msat = try_msat
                update = forward.forward_step(n.data, a_prime)
                n.add_child(update)
                n = n.children[n.i]
                k += 1
        elif found:
            winner = n.data
            xprint("Agreement found! P wins the game.")
            break
        else:
            # Forward move
            xprint("No contradiction or agreement found, will apply forward move")
            get_m()

            update = forward.forward_step(n.data, a_prime)
            n.add_child(update)
            n = n.children[0]
            k += 1

    # End of the game: print search tree, winning interpretation if it exists, and YES/NO
    if myfun.pc:
        print("-------------------")
        print("Search tree:")

        while type(n) is not tree.Root:
            n = n.parent
        tree.traverse(n, 0)

        print("-------------------")
        if winner != '':
            string = ''
            for j, w in enumerate(winner):
                if w != 'u':
                    if string != '':
                        string = string + ','
                    else:
                        string = string + '{'
                    string = string + myfun.arguments[j].name + '->' + w
            print("Interpretation: %s " % string+'}')
        print("-------------------")
    if winner != '':
        print("YES")
    else:
        print("NO")


if __name__ == '__main__':
    if len(sys.argv) > 5 and sys.argv[5] == 'p':
        myfun.pc = True
    start_time = time.time()
    main()
    t = time.time() - start_time
    print("--- %s seconds ---" % t)
