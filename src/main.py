# !/usr/bin/python3

import sys
import os
import re
import sympy
import time
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
    user_in = 'adfex10'
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

    xprint('Arguments in ADF:')
    if myfun.pc:
        myfun.print_full_args(myfun.arguments)
    xprint("-------------------")

    # initial_claim = get_claim()
    # initial_claim = 'uut'
    initial_claim = 't' + (myfun.size-1)*'u'
    a_prime = myfun.check_info(initial_claim, myfun.size*'u')[0]
    xprint(f"v_0 = {initial_claim}")

    # choice = input("How would you like the program to compute mSATs? 0 = blacklist 1 = smart 2 = computation 3 = manually")
    choice = 1

    n = tree.Root(initial_claim)
    k = 0  # depth
    winner = ''

    forward.msat_rand = msat_fun.find_new(n.i, initial_claim, a_prime, 1)[1]
    # forward.msat_rand = msat_fun.find_new(n.i, initial_claim, a_prime, 2)
    n.black_list.append(forward.msat_rand)

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

            # Put combination of msats on blacklist
            # n.parent.black_list.append(forward.msat_rand)
            # print("blacklist: ", n.parent.black_list, "for parent ", n.parent.data, "of node", n.data)

            # n.parent.parent.black_list.append(n.parent.data)
            # latest = forward.msat_rand
            while not found_msat and type(n) is not tree.Root:
                n = n.parent
                k -= 1
                xprint(f"\t Backtracked to v_{k} = {n.data} with blacklist {n.black_list}")
                if type(n) is tree.Root:
                    par = len(n.data) * 'u'
                else:
                    par = n.parent.data

                a_prime = myfun.check_info(v=n.data, oldv=par)[0]
                # result_rand = msat_fun.find_new(n.i + 1, n.data, a_prime, 1)
                # print("result_rand:", result_rand)

                if choice == 2:
                    result_rand = msat_fun.find_new(n.i + 1, n.data, a_prime, 2)[1]
                    if result_rand != {}:
                        found_msat = True

                msat_fun.black_list = n.black_list
                new_msat = msat_fun.find_new(n.i + 1, n.data, a_prime, 1)
                result_rand = new_msat[1]
                # print("result:", result_rand)

                if new_msat[0]:
                    if new_msat[1] not in n.black_list:
                        found_msat = True
                    else:
                        while not found_msat and new_msat[0]:
                            new_msat = msat_fun.find_new(n.i + 1, n.data, a_prime, 1)
                            result_rand = new_msat[1]
                            if result_rand not in n.black_list:
                                found_msat = True
                            elif myfun.pc:
                                print("found", result_rand, "in blacklist")
                # else:
                #     print("no other options")

                # if result_rand not in n.black_list:
                #     found_msat = True
                # else:
                #     print("found", result_rand, "in blacklist")

                # # Nil is not 0
                # cnt = 0
                # while cnt < 30 and not found_msat:# and type(n) is not tree.Root:
                #     result_rand = msat_fun.find_new(n.i + 1, n.data, a_prime, 1)
                    # print("result_rand:", result_rand)
                    # cnt += 1
                    # if result_rand not in n.black_list:
                    #     found_msat = True
                    # else:
                    #     print("found", result_rand, "in blacklist")

            if not found_msat:  # i.e. we're at the root
                xprint("P loses game")
                break
            else:
                xprint("\t Found another msat!")
                n.i += 1
                # forward.msat = result
                forward.msat_rand = result_rand
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

            forward.msat_rand = msat_fun.find_new(0, n.data, a_prime, 1)[1]
            # forward.msat_rand = msat_fun.find_new(0, n.data, a_prime, 2)
            n.black_list.append(forward.msat_rand)

            update = forward.forward_step(n.data, a_prime)
            n.add_child(update)
            n = n.children[0]
            k += 1

    xprint("-------------------")
    xprint("Search tree:")
    if myfun.pc:
        while type(n) is not tree.Root:
            n = n.parent
        tree.traverse(n, 0)

    xprint("-------------------")
    if winner != '':
        string = ''
        for j, w in enumerate(winner):
            if w != 'u':
                if string != '':
                    string = string + ','
                else:
                    string = string + '{'
                string = string + myfun.find_arg(winner, j).name + '->' + w
        xprint("Interpretation: %s " % string+'}')
    xprint("-------------------")
    xprint("Bye!")


if __name__ == '__main__':
    choice = int(input("How many times would you like to run the program? "))
    if input("Would you like to print?") == 'y':
        myfun.pc = True
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
            times.append(t)
            c += 1
        # print(times)
        print("av: ", sum(times)/len(times))
