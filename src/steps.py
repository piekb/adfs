import sys
import os
import json
import sympy
from sympy import *
from sympy.logic import Not, And, Or
import re

import myfun
# as f
from myfun import *

known_msats = {}
# a_prime = []

def fail():
    print("information lost!")

def finish():
    print("next player")


# Check if oldv <= v between each step (so all v's are in fact comparable!)
def check_info(v, oldv, arguments):
    a_prime = []
    for i, val in enumerate(v):
        if (oldv[i] == 'u'):
            if (v[i] == 't' or v[i] == 'f'):
                a_prime.append(arguments[i])
        else:
            if (v[i] != oldv[i]):
                fail()
    if len(a_prime) == 0:
        finish()

    return a_prime

    # forward(v,a_prime,args)


## Find one mSAT for one argument
def find_msat(a):
    # msat = ''
    if '{}'.format(a) in known_msats.keys():
        msat = known_msats['{}'.format(a)]
    else:
        msat = input("Please give an msat for arg {arg} with condition = {ac}: ".format(arg=a.name, ac=a.ac))
        while True:
            if re.match("^[f,t,u]*$", msat) and len(msat) == myfun.size:
                known_msats['{}'.format(a)] = msat
                break
            else:
                print("Error! Input should be {size} characters from t,f, or u. No spaces".format(size=myfun.size))
                msat = input("Please give an msat for arg {arg} with condition = {ac}: ".format(arg=a.name, ac=a.ac))

    return msat


## Returns if there is any conflict in the "rest" of a-prime without the first defined value.
## Check if msatai!=msataj also a problem if msataj == u?
def no_conflict(a_prime, val_ai, arg, arguments):
    for a in a_prime:
        msat_aj = find_msat(a)
        val_aj = myfun.find_in(msat_aj, arg, arguments)
        if val_aj != 'u ' and val_aj != val_ai:
            print(val_aj)
            return False

    return True

## Returns whether or not mSATa == {a to Gamma(v)(a)},
## i.e. false if any other arg is defined, or if {a to not Gamma(v)(a)}
def just_one_gamma(msat, v, arg, arguments):
    for i, value in enumerate(msat):
        if arguments[i] != arg and value != 'u':
            return False
        elif arguments[i] == arg and value != myfun.find_in(myfun.gamma(v, arguments), arg, arguments):
            return False
    return True


def third(arg, v, arguments, a_prime):
    # print('third condition')
    msat_arg = find_msat(arg)
    if just_one_gamma(msat_arg, v, arg, arguments):
        return False
    else:
        for c in arg.ac.atoms():
            val_a_c = myfun.find_in(msat_arg, c, arguments)
            if not no_conflict(a_prime, val_a_c, c, arguments):
                return False
    return True


def fourth(a_prime, v, arg, arguments):
    # print('fourth condition')
    for a in a_prime:
        msat_ai = find_msat(a)
        val = myfun.find_in(msat_ai, arg, arguments)
        if val == 't' or val == 'f':
            if no_conflict(a_prime, val, arg, arguments):
                return True, msat_ai
    return False, 0


def delta(v, a_prime, arg, arguments):
    update = ''
    truth_val = myfun.find_in(v, arg, arguments)
    if truth_val == 't' or truth_val == 'f':
        if not (arg in a_prime):
            myfun.print_args(a_prime)
            update = truth_val
        elif myfun.eval_exp(arg.ac, v, arguments) == True or myfun.eval_exp(arg.ac, v, arguments) == False:
            update = truth_val
        elif third(arg, v, arguments, a_prime):
            update = truth_val
        else:
            update = 'u'
    elif truth_val == 'u':
        four = fourth(a_prime, v, arg, arguments)
        if four[0]:
            msat = four[1]
            update = myfun.find_in(msat, arg, arguments)
        else:
            update = 'u'

    return update


## Forward move
## Evaluate AC of all a in A-prime
def forward(v, a_prime, args):
    updated_acs = []
    for a in a_prime:
        updated_acs.append(myfun.eval_exp(a.ac, v, args))
    myfun.print_acs(updated_acs)

    out = ''
    for a in args:
        out = out + delta(v, a_prime, a, args)

    print(out)