from typing import Dict, Any, Union

import myfun
import ext
import random

from myfun import *
from ext import *

black_list = []


def xprint(string):
    if myfun.pc == True:
        print(string)


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
        print("inters: ", ext.inters)
        inters = ext.gen_inters(myfun.size)
        for j, inter in enumerate(inters):
            sat = inter[:a.dex] + 'u' + inter[a.dex:]
            if satisfies(v, sat, a):
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


def find_new(i, v, a_prime, choice):
    msat = {}
    other_option = False
    # arg = a_prime[0]
    if choice == 3:
        # do not use
        msat = msat_manual(i, v, a_prime)
    elif choice == 2:
        msat = msat_comp(i, v, a_prime)
        if msat != {}:
            other_option = True
    elif choice == 1:
        other = {}
        option_havers = []
        for a in a_prime:
            result = msat_smart(v, a)
            msat[f"{a.name}"] = result[1]
            other[f"{a.name}"] = result[0]

            if result[0]:
                other_option = True
                option_havers.append(a)
        if myfun.pc:
            if other_option and msat in black_list:
                print("found", msat, "in blacklist", black_list)
            elif other_option:
                print("found", msat, "which is not in blacklist")
            else:
                print("there is no other option already")
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

    # print(msat)
    return other_option, msat, option_havers


# Not super low complexity I think
def minimal(v, sat, arg):
    msat = sat[0]
    par_in = sat[1]

    ext.inters = []
    ext.allKLengthRec(['u', 't', 'f'], "", 3, len(par_in))
    op = ext.inters[1:]
    # print("over parents:", op)
    random.shuffle(op)
    new = []
    for inter in op:
        # print(inter)
        new_m = ''
        j = 0
        for i, _ in enumerate(v):
            if i in par_in:
                new_m += inter[j]
                j += 1
            else:
                new_m += 'u'
        # print("new_m:", new_m)
        if satisfies(v, new_m, arg):
            new.append(new_m)

        # if new_m.count('u') > msat.count('u'):
        #     if satisfies(v, new_m, arg):
        #         msat = new_m
    msats = min_info(new)
    if myfun.pc:
        print(msats)
    msat = random.choice(msats)

    return msat


    # Generate all strings of correct length, minus the assignment arg -> u
    # inters = ext.gen_inters(myfun.size)
    # random.shuffle(inters)
    #
    # for inter in inters:
    #     # Add the assignment arg -> u
    #     new_sat = inter[:arg.dex] + 'u' + inter[arg.dex:]
    #
    #     if new_sat.count('u') > compare.count('u'):
    #         if satisfies(v, new_sat, arg):
    #             msat = new_sat
    #             compare = new_sat
    #
    # if msat == '':
    #     msat = sat
    #
    # return msat


def satisfies(v, new_v, a):
    v_a = myfun.find_in(v, a)
    gam_a = myfun.find_in(myfun.gamma(new_v), a)
    # xprint(f"for arg {a.name} v({a.name}) = {v_a}")
    # xprint(f"for arg {a.name} gamma({a.name}) = {gam_a}")
    return v_a == gam_a


def msat_random(v, a):
    sat = ''
    par_in = []

    for j, arg in enumerate(v):
        if myfun.find_arg(v, j).sym in a.ac.atoms():
            choices = ['u', 't', 'f']
            sat = sat + random.choice(choices)
            par_in.append(j)
        else:
            sat = sat + 'u'

    # print("random: ", msat)
    return sat, par_in


# If phi is true or false
#   If this is the second retry, no other msats exist
# Else, find some random msat
def msat_smart(v, a):
    phi_a = myfun.phi(a.ac, v)
    # print(len(a.ac.atoms()))

    # print(phi_a)
    if phi_a == True or phi_a == False:
        # Second condition of mSAT_F
        msat = myfun.just_one_gamma(v, a)
        return False, msat
    else:
        while True:
            rand = msat_random(v, a)
            if satisfies(v, rand[0], a):
                break
        sat = rand[0]
        msat = minimal(v, rand, a)
    if myfun.pc:
        print("minimal:", msat, "for argument", a.name, ":", a.ac)

    # print("smart: ", msat)
    return True, msat

# IDEA: for parents(a), find indices --> make msat with u's and rand(t,f) in those places. Try until satisfiable.
# Won't be absolutely minimal though... find all then find minimal? Not sure if still too complex
# Find random msat, but keep track of which have been used and rejected
