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
prime_known_msats = {}
i = 0
min_prime = []
msats = {}


# Returns the set of mSAT interpretations from a list of SAT interpretations.
def min_info(sats):
    min_sats = []
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
            min_sats.append(w)

    min_sats.reverse()
    return min_sats


# Generates set of minimal satisfiable interpretations for argument a under interpretation v.
def gen_msats(v, a):
    sats = []
    phi_a = myfun.phi(a.ac, v)
    if phi_a == True or phi_a == False:
        # Second condition of mSAT_F
        sats.append(just_one_gamma(v, a))
    else:
        inters = ext.gen_inters(myfun.size)
        arg_in = myfun.dex(a.name)
        for j, inter in enumerate(inters):
            sat = inter[:arg_in] + 'u' + inter[arg_in:]
            v_a = myfun.find_in(v, a)
            gam_a = myfun.find_in(myfun.gamma(sat), a)
            # print(f"for arg {a.name} v({a.name}) = {v_a}")
            # print(f"for arg {a.name} gamma({a.name}) = {gam_a}")

            if v_a == gam_a:
                sats.append(sat)

    min_sats = min_info(sats)
    return min_sats


def find_msat(v, a):
    # phi_a = myfun.phi(a.ac, v)
    if f'{a.name}' in msats.keys():
        msat = msats[f'{a.name}'][i]
        if len(msats[f'{a.name}']) <= i:
            print("Hey, that doesn't exist!")
            # print(f"heya, msat for {a.name} is {msats[f'{a.name}'][i]}")
            msat = msats[f'{a.name}'][0]
        # else:
        #     print("i = 0 hoor rustig maar tijger")
        #     print(f"heya, msat for {a.name} is {msats[f'{a.name}'][0]}")

    # if f'{a}' in known_msats.keys():
    #     msat = known_msats[f'{a}']
    # else:
    #     min_sats = gen_msats(v, a)
    #     if phi_a == True or phi_a == False or len(min_sats) == 0:
    # Second condition of mSAT_F
    # msat = just_one_gamma(v, a)
    # else:
    #     if len(min_sats) > i:
    #         print(f"hey, i = {i}, m = {min_sats[i]}")
    # msat = min_sats[i]
    # else:
    #     print("wuh oh")
    #     msat = min_sats[0]
    # known_msats[f'{a}'] = msat

    return msat


# Returns if there is any conflict in the "rest" of a-prime without the first defined value.
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
    # if gam.count('u') == myfun.size:
    #     print("Gamma is also undecided")

    return gam


# Argument is in a-prime
def third(v, a_prime, a):
    phi_a = myfun.phi(a.ac, v)
    msat_arg = find_msat(v, a)
    # print(f"Finding msat for argument {a.name}, is it in aprime? {a in a_prime}")
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
            msat = four[1]
            update = myfun.find_in(msat, a)
        else:
            # print("fifth condition delta")
            update = 'u'

    return update


# Forward move
# Q: should updated ac's be passed or just per function?
def forward_step(v, a_prime):
    global msats, prime_known_msats, i
    i = 0
    # updated_acs = []
    prime_known_msats = {}
    for a in a_prime:
        # updated_acs.append(myfun.phi(a.ac, v))
        prime_known_msats[f'{a.name}'] = gen_msats(v, a)
    # print("keys:")
    # print(list(prime_known_msats.keys()))
    # print("values:")
    # print(list(prime_known_msats.values()))
    # print(updated_acs)

    msats = ext.combine_msats(prime_known_msats)
    print(msats)
    num = len(ext.full)
    # print("that's all")

    deltas = []
    # for _ in a_prime:
    while i < num:
        out = ''
        for a in myfun.arguments:
            # print(f"Delta of argument {a.name}")
            out = out + delta(v, a_prime, a)
        deltas.append(out)
        i += 1

    print(deltas)
    print("Final delta:")
    out = deltas[0]
    print(out)
    # return out
    return deltas
