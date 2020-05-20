# !/usr/bin/python3

import sys
import os
import json
import sympy
from sympy import *
from sympy.logic import Not,And,Or
from sympy.abc import A
import re

class Argument:
    name = ""
    ac = ""

# def reg():
    # test = 'not(and(a,b))'
    # pat = 'not\((.+)\)'
    # found = re.match(pat,test)
    # comp = re.compile(pat)
    # sub = comp.search(test)
    # print(sub.group(1))

    # if found:
    #     print("yay!")

    # print(Not(And(x,a)))

def rewrite(ac):
    # ac = 'neg(and(or(a,b),c))'
    neg = ac.replace('neg','Not')
    also = neg.replace('and','And')
    last = also.replace('or','Or')
    # print(last)

    ## There must be a better way to do this
    return Not(Not(last))

def main(argv):
    print("hello!")

    cur_path = os.path.dirname(__file__)
    # print(cur_path)

    part = os.path.split(cur_path)[0]
    # print(sys.argv[1])

    ## user_in = input("please enter file name: ")
    user_in = 'adfex2'
    path = part+'/ex/'+user_in
    # print(path)

    arguments = []
    set_args = []

    with open(path, 'r') as f:
        contents = f.readlines()
        size = 0
        for line in contents:
            if (line[0]=='s'):
                a = Argument()
                a.name = line[2]
                arg = sympy.symbols('{}'.format(line[2]))

                set_args.append(arg)

                arguments.append(a)
                size+=1
            elif (line[0:2]=='ac'):
                for a in arguments:
                    if (a.name == line[3]):
                        # print(line[5:(len(line)-3)])
                        a.ac = rewrite(line[5:(len(line)-3)])
            else:
                print("what?")

        print('arguments:')
        for a in arguments:
            print(a.name)
            print(a.ac)
            print('---')

    # for argu in set_args:
    #     print(Not(argu))

    ## initial_claim = input("please enter initial claim: ")


    print("bye!")

if __name__ == '__main__':
    main(sys.argv)