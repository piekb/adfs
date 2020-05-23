# !/usr/bin/python3

import sys
import os, re
import json
import sympy
from sympy import *
from sympy.logic import Not, And, Or
# import re
import myfun
from myfun import *
import steps
from steps import *

# arguments = []

class Argument:
    name = ""
    ac = ""
    sym = 0

def rewrite(ac):
    # ac = 'neg(and(or(a,b),c))'
    neg = ac.replace('neg', 'Not')
    also = neg.replace('and', 'And')
    last = also.replace('or', 'Or')
    # print(last)

    ## There must be a better way to do this, but for now this works.
    ## Alternatively, And(True,last) or Or(False,last)
    return Not(Not(last))


def main(argv):
    print("hello!")

    cur_path = os.path.dirname(__file__)
    # print(cur_path)

    part = os.path.split(cur_path)[0]
    # print(sys.argv[1])

    ## user_in = input("please enter file name: ")
    user_in = 'adfex2'
    path = part + '/ex/' + user_in
    # print(path)

    arguments = []

    with open(path, 'r') as c:
        contents = c.readlines()
        # size = 0
        for line in contents:
            if line[0] == 's':
                a = Argument()
                a.name = line[2]
                arg = sympy.symbols('{}'.format(line[2]))
                a.sym = arg
                arguments.append(a)
                myfun.size += 1
            elif line[0:2] == 'ac':
                for a in arguments:
                    if a.name == line[3]:
                        # print(line[5:(len(line)-3)])
                        a.ac = rewrite(line[5:(len(line) - 3)])
            else:
                print("what?")

        print('arguments:')
        myfun.print_full_args(arguments)

    initial_claim = input("Please enter initial claim: ")
    while True:
        if re.match("^[f,t,u]*$", initial_claim) and len(initial_claim) == myfun.size:
            break
        else:
            print("Error! Input should be {size} characters from t,f, or u. No spaces".format(size=myfun.size))
            initial_claim = input("Please enter initial claim: ")

    # print(myfun.eval_exp(arguments[0].ac,initial_claim,set_args))
    # f.gamma(initial_claim, arguments)

    print(gamma(initial_claim, arguments))

    a_prime = steps.check_info(initial_claim,'uuu',arguments)
    print("recently presented:")
    myfun.print_args(a_prime)
    print('---')

    first = steps.forward(initial_claim, a_prime, arguments)
    a_prime = steps.check_info(first, initial_claim, arguments)
    second = steps.forward(first, a_prime, arguments)
    a_prime = steps.check_info(second, first, arguments)

    print("-------------------")

    # print(myfun.gamma('ttf', arguments))

    # print(myfun.find_in(myfun.gamma(initial_claim, arguments), arguments[0], arguments))
    # print(steps.find_msat(arguments[0]))
    # g = steps.just_one_gamma(initial_claim, arguments[0], arguments)
    # print("a = just one gamma? ")
    # print(g)
    #
    # g = steps.just_one_gamma(initial_claim, arguments[1], arguments)
    # print("b = just one gamma? ")
    # print(g)
    # for c in arguments[0].ac.atoms():
    #     print(c)
    #
    # test1 = 'hello'
    # test2 = test1[:3] + 'Fu ' + test1[3:]
    # print(test2)
    #
    # steps.gen_msats(arguments[2], initial_claim, arguments)

    print("bye!")


if __name__ == '__main__':
    main(sys.argv)
