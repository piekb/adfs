# !/usr/bin/python3

import sys
import os
import re
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


class Argument:
    name = ""
    ac = ""
    sym = 0
    dex = 0


def xprint(string):
    if myfun.pc:
        print(string)


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
    xprint("Hello!")

    # Get current working directory and append exercise input file to it
    cur_path = os.getcwd()
    part = os.path.split(cur_path)[0]

    # user_in = input("Please enter file name: ")
    # print(sys.argv[1])
    user_in = 'adfex15'
    path = part + '/ex/' + user_in
    # print(path)

    myfun.size = 0
    myfun.arguments = []

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
                        # print(a.dex, a.name, a.sym)
                        # print(sympy.symbols(f"{a.name}"))
                        # print("line:", line[line.find(',')+1:(len(line) - 3)])
                        a.ac = rewrite(line[line.find(',')+1:(len(line) - 3)])
            else:
                print("Something's wrong with your input file.")

    if myfun.pc:
        print('Arguments in ADF:')
        myfun.print_full_args(myfun.arguments)
        print("-------------------")

    # choice = input("How should the program find mSATs? 0 = computation 1 = completely random")

    # initial_claim = get_claim()
    # initial_claim = 'uut'
    initial_claim = 't' + (myfun.size-1)*'u'
    a_prime = myfun.check_info(initial_claim, myfun.size*'u')[0]
    xprint(f"v_0 = {initial_claim}")

    n = tree.Root(initial_claim)
    k = 0  # depth
    winner = ''

    def get_m():
        n.num, n.msats = msat_fun.find_new(n.i, n.data, a_prime, 0)
        i = random.choice(range(n.num))
        forward.msat_rand = {}
        for a in a_prime:
            forward.msat_rand[f'{a.name}'] = n.msats[f'{a.name}'][i]
            n.msats[f'{a.name}'].remove(forward.msat_rand[f'{a.name}'])
        n.num -= 1
        n.black_list.append(forward.msat_rand)
    get_m()

    update = forward.forward_step(initial_claim, a_prime)
    n.add_child(update)
    n = n.children[0]
    k += 1
    while True:
        xprint(f"v_{k} = {n.data}")
        a_prime, contra, found = myfun.check_info(n.data, n.parent.data)
        if contra:
            if type(n.parent) is tree.Root:
                print("Initial claim already gives a contradiction, P loses game")
                break

            xprint("Contradiction found, will apply backward move")
            found_msat = False

            while not found_msat and type(n) is not tree.Root:
                n = n.parent
                k -= 1
                xprint(f"\t Backtracked to v_{k} = {n.data} with blacklist {n.black_list}")
                if type(n) is tree.Root:
                    par = len(n.data) * 'u'
                else:
                    par = n.parent.data

                a_prime = myfun.check_info(v=n.data, oldv=par)[0]

                # msat_fun.black_list = n.black_list
                if n.msats[f'{a_prime[0].name}']:
                    i = random.choice(range(n.num))
                    # print("chose", i, "for i")
                    # print(n.msats)
                    try_msat = {}
                    for a in a_prime:
                        try_msat[f'{a.name}'] = n.msats[f'{a.name}'][i]
                        n.msats[f'{a.name}'].remove(try_msat[f'{a.name}'])
                    n.num -= 1

                    if try_msat not in n.black_list:
                        found_msat = True
                    else:
                        print("what?", try_msat, n.black_list, n.msats)

            if not found_msat:  # i.e. we're at the root
                xprint("P loses game")
                break
            else:
                xprint("\t Found another msat!")
                n.i += 1
                # forward.msat = result
                # forward.msat_rand = result_rand
                forward.msat_rand = try_msat
                n.black_list.append(forward.msat_rand)
                update = forward.forward_step(n.data, a_prime)
                n.add_child(update)
                n = n.children[n.i]
                k += 1
        elif found:
            winner = n.data
            xprint("Agreement found! P wins the game.")
            break
        else:
            xprint("No contradiction or agreement found, will apply forward move")

            get_m()

            update = forward.forward_step(n.data, a_prime)
            n.add_child(update)
            n = n.children[0]
            k += 1

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
                    string = string + myfun.find_arg(winner, j).name + '->' + w
            print("Interpretation: %s " % string+'}')
        print("-------------------")
        print("Bye!")
    if winner != '':
        print("YES")
    else:
        print("NO")


if __name__ == '__main__':
    # myfun.pc = True
    # start_time = time.time()
    # main(sys.argv)
    # t = time.time() - start_time
    # print("--- %s seconds ---" % t)

    # choice = int(input("How many times would you like to run the program? "))
    choice = 50
    # if input("Would you like to print?") == 'y':
    #     myfun.pc = True
    if choice < 1:
        print("Okay, bye")
    elif choice == 1:
        start_time = time.time()
        main(sys.argv)
        t = time.time() - start_time
        print("--- %s seconds ---" % t)
    else:
        times = []
        c = 0
        while c < choice:
            start_time = time.time()
            main(sys.argv)
            t = time.time() - start_time
            # print(t)
            times.append(t)
            c += 1
        # print(times)
        print("Average computation time: ", sum(times)/len(times))
