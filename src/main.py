# !/usr/bin/python3

import sys
import os
# import logic
# import json
# import re
# import spacy
# from pathlib import Path

class Argument:
    name = ""
    ac = ""


def main(argv):
    print("hello!")

    cur_path = os.path.dirname(__file__)
    # print(cur_path)

    part = os.path.split(cur_path)[0]
    # print(sys.argv[1])

    # user_in = input("please enter file name:")
    user_in = 'adfex2'
    path = part+'/ex/'+user_in
    # print(path)

    arguments = []

    with open(path, 'r') as f:
        contents = f.readlines()
        # print(contents)
        for line in contents:
            # print(i)
            # print(line[0:2])
            # print(line[2:(len(line) - 3)])
            # print('---')
            if (line[0]=='s'):
                a = Argument()
                a.name = line[2]
                arguments.append(a)
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




    print("bye!")

if __name__ == '__main__':
    main(sys.argv)