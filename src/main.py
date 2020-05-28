# !/usr/bin/python3

import sys
import os, re
import json
import sympy
from sympy import *
from sympy import simplify
from sympy.logic import Not, And, Or, Implies, Equivalent
# import re
import myfun
from myfun import *
import forward
from forward import *


class Argument:
    name = ""
    ac = ""
    sym = 0
    dex = 0


def rewrite(ac):
    # ac = 'neg(and(or(a,b),c))'
    iff = ac.replace('iff', 'Equivalent').replace('imp', 'Implies').replace('neg', 'Not')
    tf = iff.replace('and', 'And').replace('or', 'Or').replace('c(v)', 'True').replace('c(f)', 'False')
    # print(tf)

    ## There might be a better way to do this, but for now this works.
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
    claim = input("Please enter the truth value of argument {} in initial claim: ".format(init_arg))
    while True:
        if myfun.dex(init_arg) != None and re.match("^[f,t]*$", claim):
            break
        elif re.match("^[f,t]*$", claim):
            print("Error! Argument does not exist")
            init_arg = input("Please enter argument for initial claim: ")
        else:
            print("Error! A truth value is t or f. ")
            claim = input("Please enter the truth value of argument {} in initial claim: ".format(init_arg))

    initial_claim = myfun.make_one(claim, init_arg)

    print("initial claim: ")
    print(initial_claim)

    return initial_claim


def main(argv):
    print("hello!")

    cur_path = os.path.dirname(__file__)
    # print(cur_path)

    part = os.path.split(cur_path)[0]
    # print(sys.argv[1])

    # user_in = input("please enter file name: ")
    user_in = 'adfex2'
    path = part + '/ex/' + user_in
    # print(path)

    with open(path, 'r') as c:
        contents = c.readlines()
        # size = 0
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
                        # print(line[5:(len(line)-3)])
                        a.ac = rewrite(line[5:(len(line) - 3)])
            else:
                print("what?")

        print('arguments in ADF:')
        myfun.print_full_args(myfun.arguments)

    print("-------------------")
    initial_claim = get_claim()

    a_prime = myfun.check_info(initial_claim, myfun.make_one('u', 'a'))[0]
    print("recently presented:")
    myfun.print_args(a_prime)
    print("-------------------")

    first = initial_claim
    second = forward.forward_step(initial_claim, a_prime)
    while True:
        a_prime, contra, found = myfun.check_info(second, first)
        if contra:
            # found contradiction, need to apply backward move
            print("found a contradiction, need to apply backward move")
            break
        elif found:
            # found agreement
            print("agreement found!")
            break
        else:
            print("no contradiction, no agreement found")
            first = second
            second = forward.forward_step(first, a_prime)


    # first = forward.forward_step(initial_claim, a_prime)
    # a_prime = myfun.check_info(first, initial_claim)
    # second = forward.forward_step(first, a_prime)
    # a_prime = myfun.check_info(second, first)

    print("-------------------")

    # x, y = sympy.symbols('x,y')
    # test = rewrite('iff(neg(x),or(neg(x),and(y,c(f))))')
    # print(test.subs({x: True}))
    # print(simplify(arguments[0].ac))

    # print(forward.find_msat(arguments[0]))

    # g = forward.just_one_gamma(initial_claim, arguments[0], arguments)
    # print("a = just one gamma? ")
    # print(g)

    # g = forward.just_one_gamma(initial_claim, arguments[1], arguments)
    # print("b = just one gamma? ")
    # print(g)

    # forward.gen_msats(arguments[2], initial_claim, arguments)

    print("bye!")


if __name__ == '__main__':
    main(sys.argv)
