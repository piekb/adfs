import sys
import os
import json
import sympy
from sympy import *
import re
import myfun
from myfun import *
import ext
from ext import *

# msat = {}
msat_rand = {}


def find_msat(a):
    # return msat_rand
    return msat_rand[f"{a.name}"]


# Returns whether there is any conflict in the "rest" of a-prime without the first defined value.
def no_conflict(msat_ai, a_prime, a):
    val_ai = myfun.find_in(msat_ai, a)
    for a_j in a_prime:
        msat_aj = find_msat(a_j)
        val_aj = myfun.find_in(msat_aj, a)
        if val_aj != 'u' and val_ai != 'u' and val_aj != val_ai:
            print(f'Found a conflict: val_ai = {val_ai}, val_aj = {val_aj} for arg {a.name} on arg {a.name}')
            return False
    return True


# Argument is in a-prime
def third(v, a_prime, a):
    phi_a = myfun.phi(a.ac, v)
    msat_arg = find_msat(a)
    if msat_arg == myfun.just_one_gamma(v, a):
        return False
    else:
        for c in phi_a.atoms():
            # val_a_c = myfun.find_in(msat_arg, c)
            if not no_conflict(msat_arg, a_prime, c):
                print("- conflict found -")
                return False
    return True


def fourth(v, a_prime, a):
    for a_i in a_prime:
        msat_ai = find_msat(a_i)
        print(msat_ai)
        val = myfun.find_in(msat_ai, a)

        # Clean up, now there's a double finding val in msat_ai
        if val == 't' or val == 'f':
            if no_conflict(msat_ai, a_prime, a):
                return True, msat_ai
    return False, 0


def delta(v, a_prime, a):
    update = ''
    truth_val = myfun.find_in(v, a)
    if truth_val == 't' or truth_val == 'f':
        if not (a in a_prime):
            # print("first condition delta")
            update = truth_val
        elif (myfun.phi(a.ac, v) == True and truth_val == 't') or (myfun.phi(a.ac, v) == False and truth_val == 'f'):
            # print("second condition delta")
            update = truth_val
        elif third(v, a_prime, a):
            # print("third condition delta")
            update = truth_val
        else:
            # print("fifth condition delta")
            update = 'u'
    elif truth_val == 'u':
        four = fourth(v, a_prime, a)
        if four[0]:
            # print("fourth condition delta")
            msat_f = four[1]
            update = myfun.find_in(msat_f, a)
        else:
            # print("fifth condition delta")
            update = 'u'

    return update


# Forward move
def forward_step(v, a_prime):
    out = ''
    for a in myfun.arguments:
        # print(f"Delta of argument {a.name}")
        out = out + delta(v, a_prime, a)
    # print("Final delta:", out)
    return out
