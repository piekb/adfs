import sys
import os
import json
import sympy
from sympy import *
from sympy.logic import Not, And, Or
import re
import myfun
from myfun import *
import ext
from ext import *

known_msats = {}
# a_prime = []

def finish():
    print("agreement found!")

# Check if oldv <= v between each step (so all v's are in fact comparable!)
def check_info(v, oldv, arguments):
    a_prime = []
    fail = False
    for i, val in enumerate(v):
        if (oldv[i] == 'u'):
            if (v[i] == 't' or v[i] == 'f'):
                a_prime.append(arguments[i])
        else:
            if (v[i] != oldv[i]):
                fail = True
    if fail:
        print("contradiction!")
    elif len(a_prime) == 0:
        finish()
    return a_prime

    # forward(v,a_prime,args)

def gen_msats(a, v, arguments):
    inters = ext.gen_inters(myfun.size)
    print('before:')
    print(inters)
    sats = []
    print(sats)
    arg_in = myfun.dexin(v, a, arguments)

    for i, inter in enumerate(inters):
        newsat = inter[:arg_in] + 'u' + inter[arg_in:]
        print(newsat)
        sats[i] = newsat

    # for i, sat in enumerate(sats):
    #     v_a = myfun.find_in(v, a, arguments)
    #     gam_a = myfun.find_in(myfun.gamma(sat, arguments), a, arguments)
    #     if v_a != gam_a:
    #
    #         sats.remove(sat)

    # print(inters)
    # print(sats)

def msat(a, phi_a, v, args):
    if '{}'.format(a) in known_msats.keys():
        msat = known_msats['{}'.format(a)]
    else:
        gen_msats(a, v, args)
        if phi_a == True or phi_a == False: #or len(msats[a,v])==0:
            msat = just_one_gamma(v, a, args)
        else:
            # msat = msats[a,v][0]
            msat = just_one_gamma(v, a, args)
        known_msats['{}'.format(a)] = msat
    return msat


## Find one mSAT for one argument
def find_msat(a):
    # msat = ''
    if '{}'.format(a) in known_msats.keys():
        msat = known_msats['{}'.format(a)]
    else:
        msat = input("Please give an msat w for arg {arg} with condition = {ac} such that gamma(w)({arg}) = v({arg}): ".format(arg=a.name, ac=a.ac))
        while True:
            if re.match("^[f,t,u]*$", msat) and len(msat) == myfun.size: #and myfun.find_in(v, a, arguments) == myfun.find_in(gamma(v, arguments), a, arguments)
                known_msats['{}'.format(a)] = msat
                break
            else:
                print("Error! Input should be {size} characters from t,f, or u. No spaces".format(size=myfun.size))
                msat = input("Please give an msat w for arg {arg} with condition = {ac} such that gamma(w)({arg}) = v({arg}): ".format(arg=a.name, ac=a.ac))

    return msat


## Returns if there is any conflict in the "rest" of a-prime without the first defined value.
## Check if msatai!=msataj also a problem if msataj == u?
def no_conflict(a_prime, val_ai, arg, arguments):
    for a in a_prime:
        msat_aj = find_msat(a)
        val_aj = myfun.find_in(msat_aj, arg, arguments)
        if val_aj != 'u' and val_aj != val_ai:
            print(val_aj)
            return False

    return True

## Returns {a to Gamma(v)(a)}
def just_one_gamma(v, arg, arguments):
    msat = ''
    for i, value in enumerate(msat):
        # if arguments[i] != arg and value != 'u':
        #     return False
        # elif arguments[i] == arg and value != myfun.find_in(myfun.gamma(v, arguments), arg, arguments):
        #     return False
        if arguments[i] == arg:
            msat[i] = myfun.find_in(myfun.gamma(v, arguments), arg, arguments)
        else:
            msat[i] = 'u'
    return msat


def third(arg, v, arguments, a_prime):
    print('third condition')
    msat_arg = find_msat(arg)
    if msat_arg == just_one_gamma(v, arg, arguments):
        return False
    else:
        for c in arg.ac.atoms():
            val_a_c = myfun.find_in(msat_arg, c, arguments)
            if not no_conflict(a_prime, val_a_c, c, arguments):
                return False
    return True


def fourth(a_prime, v, arg, arguments):
    print('fourth condition')
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
        elif myfun.phi(arg.ac, v, arguments) == True or myfun.phi(arg.ac, v, arguments) == False:
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
        updated_acs.append(myfun.phi(a.ac, v, args))
    myfun.print_acs(updated_acs)

    out = ''
    for a in args:
        out = out + delta(v, a_prime, a, args)

    print(out)
