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

known_msats = {}


## Returns the set of mSAT interpretations from a list of SAT interpretations.
def min_info(sats):
    msats = []
    d = dict.fromkeys(sats, 1)
    for i, sat in enumerate(sats):
        count = 0
        for j, tv in enumerate(sat):
            if tv != 'u':
                count += 1
        d[f'{sat}'] = count

    sort = sorted(d, key=d.get)
    for w in sort:
        # print(w, d[w])
        if d[w] == d[sort[0]]:
            msats.append(w)

    return msats


## Generates set of minimal satisfiable interpretations for argument a under interpretation v.
def gen_msats(v, a):
    inters = ext.gen_inters(myfun.size)
    sats = []
    arg_in = myfun.dex(a.name)

    for i, inter in enumerate(inters):
        sat = inter[:arg_in] + 'u' + inter[arg_in:]
        v_a = myfun.find_in(v, a)
        gam_a = myfun.find_in(myfun.gamma(sat), a)
        # print(f"for arg {a.name} v({a.name}) = {v_a}")
        # print(f"for arg {a.name} gamma({a.name}) = {gam_a}")

        if v_a == gam_a:
            sats.append(sat)

    msats = min_info(sats)
    return msats


def find_msat(v, a):
    phi_a = myfun.phi(a.ac, v)
    if f'{a}' in known_msats.keys():
        msat = known_msats[f'{a}']
    else:
        msats = gen_msats(v, a)
        if phi_a == True or phi_a == False or len(msats) == 0:
            print("here now")
            msat = just_one_gamma(v, a)
        else:
            msat = msats[0]
        known_msats[f'{a}'] = msat

    # print(f'msat for arg {a.name} = {msat}')
    return msat


## Returns if there is any conflict in the "rest" of a-prime without the first defined value.
def no_conflict(v, a_prime, a_i):
    val_ai = myfun.find_in(v, a_i)
    for a_j in a_prime:
        msat_aj = find_msat(v, a_j)
        val_aj = myfun.find_in(msat_aj, a_i)
        if val_aj != 'u' and val_ai != 'u' and val_aj != val_ai:
            print(f'here is conflict: val_ai = {val_ai}, val_aj={val_aj} for arg {a_i.name} on arg {a_j.name}')
            return False
    return True


# Returns {a to Gamma(v)(a)}
def just_one_gamma(v, a):
    new = myfun.find_in(myfun.gamma(v), a)

    gam = myfun.make_one(new, a.name)
    if gam.count('u') == myfun.size:
        print("gamma is also undecided")

    return gam


def third(v, a_prime, a):
    phi_a = myfun.phi(a.ac, v)
    msat_arg = find_msat(v, a)
    if msat_arg == just_one_gamma(v, a):
        return False
    else:
        for c in phi_a.atoms():
            # val_a_c = myfun.find_in(msat_arg, c)
            if not no_conflict(v, a_prime, c):
                print("- conflict found -")
                return False
    return True


def fourth(v, a_prime, a):
    for a_i in a_prime:
        msat_ai = find_msat(v, a_i)
        val = myfun.find_in(msat_ai, a)

        ## Clean up, now there's a double finding val in v
        if val == 't' or val == 'f':
            if no_conflict(v, a_prime, a):
                return True, msat_ai
    return False, 0


def delta(v, a_prime, a):
    update = ''
    truth_val = myfun.find_in(v, a)
    if truth_val == 't' or truth_val == 'f':
        if not (a in a_prime):
            # print("first case in delta")
            myfun.print_args(a_prime)
            update = truth_val
        elif myfun.phi(a.ac, v) == True or myfun.phi(a.ac, v) == False:
            print("second condition delta")
            update = truth_val
        elif third(v, a_prime, a):
            print("third condition delta")
            update = truth_val
        else:
            update = 'u'
    elif truth_val == 'u':
        four = fourth(v, a_prime, a)
        if four[0]:
            print("fourth condition delta")
            msat = four[1]
            update = myfun.find_in(msat, a)
        else:
            update = 'u'

    return update


# Forward move
# Q: should updated ac's be passed or just per function?
def forward_step(v, a_prime):
    updated_acs = []
    for a in a_prime:
        updated_acs.append(myfun.phi(a.ac, v))
    # myfun.print_acs(updated_acs)

    out = ''
    for a in myfun.arguments:
        print(f"for argument {a.name}")
        out = out + delta(v, a_prime, a)

    print("final delta:")
    print(out)
    return out
