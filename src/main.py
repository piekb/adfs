# !/usr/bin/python3

import sys
import os
import re
import json
import sympy
import myfun
import forward
import tree

from sympy import *
from myfun import *
from forward import *
from tree import *


class Argument:
    name = ""
    ac = ""
    sym = 0
    dex = 0


def rewrite(ac):
    iff = ac.replace('iff', 'Equivalent').replace('imp', 'Implies').replace('neg', 'Not')
    tf = iff.replace('and', 'And').replace('or', 'Or').replace('c(v)', 'True').replace('c(f)', 'False')

    # There might be a better way to convert a string to a formula, but for now this works.
    return simplify(tf)


def get_claim():
    # initial_claim = input("Please enter initial claim: ")
    # while True:
    #     if re.match("^[f,t,u]*$", initial_claim) and len(initial_claim) == myfun.size:
    #         break
    #     else:
    #         print("Error! Input should be {size} characters from t,f, or u. No spaces".format(size=myfun.size))
    #         initial_claim = input("Please enter initial claim: ")

    init_arg = input("Please enter argument for initial claim: ")
    claim = input(f"Please enter the truth value of argument {init_arg} in initial claim: ")
    while True:
        if myfun.dex(init_arg) is not None and re.match('[f,t]', claim):
            break
        elif re.match('[f,t]', claim):
            print("Error! Argument does not exist")
            init_arg = input("Please enter argument for initial claim: ")
        else:
            print("Error! A truth value is t or f. ")
            claim = input(f"Please enter the truth value of argument {init_arg} in initial claim: ")

    initial_claim = myfun.make_one(claim, init_arg)
    print(f"Initial claim: {initial_claim}")
    return initial_claim

def main(argv):
    print("Hello!")

    cur_path = os.path.dirname(__file__)
    part = os.path.split(cur_path)[0]

    # user_in = input("please enter file name: ")
    user_in = 'adfex6'
    path = part + '/ex/' + user_in
    # print(path)

    with open(path, 'r') as c:
        contents = c.readlines()
        for line in contents:
            if line[0] == 's':
                a = Argument()
                a.name = line[2]
                a.sym = sympy.symbols('{}'.format(a.name))
                a.dex = myfun.size

                myfun.size += 1
                myfun.arguments.append(a)
            elif line[0:2] == 'ac':
                for a in myfun.arguments:
                    if a.name == line[3]:
                        a.ac = rewrite(line[5:(len(line) - 3)])
            else:
                print("Something's wrong with your input file, dude.")

    print('Arguments in ADF:')
    myfun.print_full_args(myfun.arguments)
    print("-------------------")

    initial_claim = get_claim()
    a_prime = myfun.check_info(initial_claim, myfun.make_one('u', 'a'))[0]
    print("-------------------")

    first = initial_claim
    second = forward.forward_step(initial_claim, a_prime)#[0]
    n = tree.Root(first)
    n.add_child(second)
    # for i, c in enumerate(second):
    #     n.add_child(c)


    while True:
        a_prime, contra, found = myfun.check_info(second, first)
        if contra:
            print("Found a contradiction, will apply backward move")
            n.visited = True
            if type(n) is tree.Root:
                print("P loses game")
                break
            else:
                for c in n.children:
                    print(c.data)
                # n = n.parent
                # print("hello the parent is here")
                # forward.i += 1
                # second = forward.forward_step(first, a_prime)
            break
        elif found:
            print("Agreement found!")
            break
        else:
            n = n.children[0]
            print("No contradiction, no agreement found")
            first = second
            second = forward.forward_step(first, a_prime)
            n.add_child(second)
            n.add_child('other')
            # for i, c in enumerate(second):
            #     n.add_child(c)

    print("Let's look at the tree so far")
    while type(n) is not tree.Root:
        n = n.parent
    tree.traverse(n, 0)

    print("-------------------")
    print("Bye!")


if __name__ == '__main__':
    main(sys.argv)
