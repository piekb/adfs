from typing import Dict, Any, Union

import myfun
import ext
import random

from myfun import *
from ext import *

black_list = []


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
        sats.append(myfun.just_one_gamma(v, a))
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


def msat_comp(i, v, a_prime):
    found_msats = {}
    for a in a_prime:
        found_msats[f'{a.name}'] = gen_msats(v, a)

    msats = ext.combine_msats(found_msats)
    msat = {}

    for a in a_prime:
        try:
            msat[f'{a.name}'] = msats[f'{a.name}'][i]
        except IndexError as error:
            print("No other mSATs, sorry!")

    # print("mSAT = ", msat)
    # print("keys:")
    # print(list(found_msats.keys()))
    # print("values:")
    # print(list(found_msats.values()))
    # print(msats)
    return msat


def find_new(i, v, a_prime, choice):
    msat = {}
    # arg = a_prime[0]
    if choice == 3:
        # do not use
        msat = msat_manual(i, v, a_prime)
    elif choice == 2:
        msat = msat_comp(i, v, a_prime)
    elif choice == 1:
        for a in a_prime:
            msat[f"{a.name}"] = msat_smart(v, a)
    elif choice == 0:
        for a in a_prime:
            msat[f"{a.name}"] = msat_smart(v, a)
        print("blacklist:", black_list)
        check = True
        frikandel = True
        frans = {}
        while msat in black_list and frikandel:
            # print("here now, sup? ")
            if check:
                print("checking once:", msat)
                check = False

            for a in a_prime:
                phi_a = myfun.phi(a.ac, v)
                print(phi_a)

                # If phi is T/F then there is no other mSAT
                if phi_a == True or phi_a == False:
                    frans[f"{a.name}"] = msat[f"{a.name}"]
                else:
                    frans[f"{a.name}"] = msat_smart(v, a)

                frans[f"{a.name}"] = msat_smart(v, a)
                # if not msat[f"{a.name}"] == frans[f"{a.name}"]:
                #     msat[f"{a.name}"] = frans[f"{a.name}"]
            if msat == frans:
                frikandel = False

    print(msat)
    return msat


def msat_manual(i, v, a_prime):
    new_msat = {}
    for a in a_prime:
        q = f"\t Please give mSAT option {i + 1} for phi({a.name}) under {v}: "
        if i > 0:
            q = f"\t \t Please give mSAT option {i + 1} for phi({a.name}) under {v}: "
        new_msat[f'{a.name}'] = input(q)

    for a in a_prime:
        if len(new_msat[f'{a.name}']) == 0:
            return {}

    return new_msat


def msat_random_smart(v, a):
    msat = ''
    phi_a = myfun.phi(a.ac, v)
    if phi_a == True or phi_a == False:
        # Second condition of mSAT_F
        msat = myfun.just_one_gamma(v, a)
    else:
        msat_random(v, a)

    print("random: ", msat)
    return msat


def msat_random(v, a):
    msat = ''
    for j, arg in enumerate(v):
        if myfun.find_arg(v, j).sym in a.ac.atoms():
            choices = ['u', 't', 'f']
            msat = msat + random.choice(choices)
        else:
            msat = msat + 'u'

    # print("random: ", msat)
    return msat


# If phi is true or false
#   If this is the second retry, no other msats exist
# Else, find some random msat
def msat_smart(v, a):
    phi_a = myfun.phi(a.ac, v)
    # print(phi_a)
    if phi_a == True or phi_a == False:
        # Second condition of mSAT_F
        msat = myfun.just_one_gamma(v, a)
    else:
        while True:
            rand = msat_random(v, a)
            v_a = myfun.find_in(v, a)
            gam_a = myfun.find_in(myfun.gamma(rand), a)
            # print(f"for arg {a.name} v({a.name}) = {v_a}")
            # print(f"for arg {a.name} gamma({a.name}) = {gam_a}")
            if v_a == gam_a:
                break
        msat = rand

    print("smart: ", msat)
    return msat

# IDEA: for parents(a), find indices --> make msat with u's and rand(t,f) in those places. Try until satisfiable.
# Won't be absolutely minimal though... find all then find minimal? Not sure if still too complex
# Find random msat, but keep track of which have been used and rejected
