# !/usr/bin/python3

import sys
import os
# import logic
# import json
# import re
# import spacy
# from pathlib import Path
import sympy
from sympy import *
import re

class Argument:
    name = ""
    ac = ""

def other():
    pattern = 'abs'
    test_string = 'abs'
    result = re.match(pattern, test_string)

    if result:
        print(pattern)

def rewrite():
    test = 'not(and(a,b))'
    pat = 'not\((.+)\)'
    found = re.match(pat,test)
    comp = re.compile(pat)
    sub = comp.search(test)
    print(sub.group(1))

    if found:
        print("yay!")

    # x,y = sympy.symbols('x,y')

def main(argv):
    print("hello!")

    cur_path = os.path.dirname(__file__)
    # print(cur_path)

    part = os.path.split(cur_path)[0]
    # print(sys.argv[1])

    # user_in = input("please enter file name: ")
    user_in = 'adfex5'
    path = part+'/ex/'+user_in
    # print(path)

    arguments = []
    # initial_claim = input("please enter initial claim: ")

    with open(path, 'r') as f:
        contents = f.readlines()
        # print(contents)
        size = 0
        for line in contents:
            if (line[0]=='s'):
                a = Argument()
                a.name = line[2]
                arguments.append(a)
                size+=1
            elif (line[0:2]=='ac'):
                # print(line[3])
                for a in arguments:
                    # print(a.name)
                    if (a.name == line[3]):
                        # print(line[5:(len(line)-3)])
                        a.ac = line[5:(len(line)-3)]
            else:
                print("what?")
        print('arguments:')
        for a in arguments:
            print(a.name)
            print(a.ac)
            print('---')

    rewrite()
    print("bye!")

if __name__ == '__main__':
    main(sys.argv)