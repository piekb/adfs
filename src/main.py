# !/usr/bin/python3

import sys
import os
import re
import sympy
import myfun
import forward
import tree
import msat_fun

from sympy import *
from myfun import *
from forward import *
from tree import *
from msat_fun import *


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


def input_claim():
    initial_claim = input("Please enter initial claim: ")
    while True:
        if re.match("^[f,t,u]*$", initial_claim) and len(initial_claim) == myfun.size:
            break
        else:
            print("Error! Input should be {size} characters from t,f, or u. No spaces".format(size=myfun.size))
            initial_claim = input("Please enter initial claim: ")
    print(f"Initial claim: {initial_claim}")
    return initial_claim


def get_claim():
    init_arg = input("Please enter argument for initial claim: ")
    claim = input(f"Please enter the truth value of argument {init_arg} in initial claim: ")
    while True:
        if myfun.dex(init_arg) is not None and re.match('^[f,t]$', claim):
            break
        elif re.match('^[f,t]$', claim):
            print("Error! Argument does not exist")
            init_arg = input("Please enter argument for initial claim: ")
        else:
            print("Error! A truth value is t or f. ")
            claim = input(f"Please enter the truth value of argument {init_arg} in initial claim: ")

    initial_claim = myfun.make_one(claim, init_arg)
    print(f"Initial claim: {initial_claim}")
    print("-------------------")
    return initial_claim


def main(argv):
    print("Hello!")

    # Get current working directory and append exercise input file to it
    cur_path = os.getcwd()
    part = os.path.split(cur_path)[0]

    # user_in = input("Please enter file name: ")
    # print(sys.argv[1])
    user_in = 'adfex7'
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
                print("Something's wrong with your input file.")

    print('Arguments in ADF:')
    myfun.print_full_args(myfun.arguments)
    print("-------------------")

    initial_claim = get_claim()
    a_prime = myfun.check_info(initial_claim, myfun.make_one('u', 'a'))[0]
    print(f"v_0 = {initial_claim}")

    # choice = input("How would you like the program to compute mSATs? 0 = blacklist 1 = smart 2 = computation 3 = manually")
    choice = 2

    n = tree.Root(initial_claim)
    k = 0  # depth

    forward.msat_rand = msat_fun.find_new(n.i, initial_claim, a_prime, 1)

    update = forward.forward_step(initial_claim, a_prime)
    n.add_child(update)
    n = n.children[0]
    k += 1
    while True:
        print(f"v_{k} = {n.data}")
        a_prime, contra, found = myfun.check_info(n.data, n.parent.data)
        if contra:
            if type(n.parent) is tree.Root:
                print("Initial claim already gives a contradiction, P loses game")
                break

            print("Contradiction found, will apply backward move")
            found_msat = False

            # Put combination of msats on blacklist
            # msat_fun.black_list.append(forward.msat_rand)
            # n.parent.parent.black_list.append(n.parent.data)

            while not found_msat and type(n) is not tree.Root:
                n = n.parent
                k -= 1
                print(f"\t Backtracked to v_{k} = {n.data}")
                if type(n) is tree.Root:
                    par = len(n.data) * 'u'
                else:
                    par = n.parent.data

                a_prime = myfun.check_info(v=n.data, oldv=par)[0]

                result_rand = msat_fun.find_new(n.i + 1, n.data, a_prime, 1)
                print("result_rand:", result_rand)
                if result_rand != forward.msat_rand:
                    found_msat = True

                # if '' not in result_rand.values():
                #     found_msat = True
                # else:
                    # No other feasible msat found:
                    # n.parent.parent.black_list.append(n.parent.data)

                    # msat_fun.black_list.append(n.data)
                    # n.black_list.append(result_rand)
                    # continue

            if not found_msat:  # i.e. we're at the root
                print("P loses game")
                break
            else:
                print("\t Found another msat!")
                n.i += 1
                # forward.msat = result
                forward.msat_rand = result_rand
                update = forward.forward_step(n.data, a_prime)
                n.add_child(update)
                n = n.children[n.i]
                k += 1
        elif found:
            print("Agreement found! P wins the game.")
            break
        else:
            print("No contradiction or agreement found, will apply forward move")

            forward.msat_rand = msat_fun.find_new(0, n.data, a_prime, 1)
            # forward.msat = msat_fun.find_new(0, n.data, a_prime, 2)

            update = forward.forward_step(n.data, a_prime)
            n.add_child(update)
            n = n.children[0]
            k += 1

    print("-------------------")
    print("Search tree:")
    while type(n) is not tree.Root:
        n = n.parent
    tree.traverse(n, 0)

    print("-------------------")
    print("Bye!")


if __name__ == '__main__':
    main(sys.argv)
