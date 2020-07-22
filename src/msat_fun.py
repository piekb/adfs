from typing import Dict, Any, Union
import myfun
import ext
import random

from myfun import *
from ext import *


# Returns whether new_v satisfies phi(a)
def satisfies(v, new_v, a):
    v_a = myfun.find_in(v, a)
    gam_a = myfun.find_in(myfun.gamma(new_v), a)
    return v_a == gam_a


# Sorts a list by informational ordering
def sort_this(list):
    d = dict.fromkeys(list, 1)
    for i, sat in enumerate(list):
        d[f'{sat}'] = sat.count('t') + sat.count('f')

    sort = sorted(d, key=d.get)
    return sort


# Returns the set of mSAT interpretations from a list of SAT interpretations.
def min_info(sats):
    min_sats = []
    d = dict.fromkeys(sats, 1)
    for i, sat in enumerate(sats):
        d[f'{sat}'] = sat.count('t')+sat.count('f')

    sort = sorted(d, key=d.get)
    # print("sorted:", sort)
    for w in sort:
        # print(w, d[w])
        if d[w] == d[sort[0]]:
            min_sats.append(w)

    min_sats.reverse()
    return min_sats


# Generates set of minimal satisfiable interpretations for argument a under interpretation v.
# Complexity optimized by bottom-up search for minimality
def msat_comp_1(v, arg):
    ext.inters = []
    num_par = len(arg.ac.atoms())
    inters = sort_this(ext.gen_inters(num_par)[1:])
    msats = []
    cnt = num_par - 1
    for inter in inters:
        if inter.count('u') < cnt:
            if msats:
                break
            else:
                # When e.g. phi(a) = b & c, just one t/f doesn't satisfy it
                cnt -= 1
        new_inter = ''
        j = 0
        # This part is still quite slow
        for i, _ in enumerate(v):
            if myfun.arguments[i].sym in arg.ac.atoms():
                new_inter += inter[j]
                j += 1
            else:
                new_inter += 'u'
        if satisfies(v, new_inter, arg):
            msats.append(new_inter)
    return msats


# Generates set of minimal satisfiable interpretations for argument a under interpretation v.
def msat_comp_2(v, arg):
    ext.inters = []
    num_par = len(arg.ac.atoms())
    inters = sort_this(ext.gen_inters(num_par)[1:])
    sats = []
    for inter in inters:
        new_inter = ''
        j = 0
        # This part is still quite slow
        for i, _ in enumerate(v):
            if myfun.arguments[i].sym in arg.ac.atoms():
                new_inter += inter[j]
                j += 1
            else:
                new_inter += 'u'
        if satisfies(v, new_inter, arg):
            sats.append(new_inter)
    msats = min_info(sats)
    return msats


# Main function of finding mSATs. Algorithm number is read from command line
def find_new(v, a_prime, alg):
    msats = {}
    for a in a_prime:
        phi_a = myfun.phi(a.ac, v)

        # Second case of mSAT_A'; there is no other mSAT
        if phi_a == True or phi_a == False:
            m = [myfun.just_one_gamma(v, a)]
            msats[f"{a.name}"] = m

        # First case of mSAT_A'
        else:
            # Smart computation over parents of a in A'
            if alg == 1:
                msats[f"{a.name}"] = msat_comp_1(v, a)
            # Computation over parents of a in A'
            elif alg == 2:
                msats[f"{a.name}"] = msat_comp_2(v, a)

    # Combine msats of different arguments to yield list of options
    result = ext.combine_msats(msats)
    num = len(result[f"{a_prime[0].name}"])
    return num, result


# UNUSED functions from here down. For posterity.

# Generates set of minimal satisfiable interpretations for argument a under interpretation v.
# Complexity optimized by bottom-up search for minimality
def msat_comp_3(v, a):
    msats = []
    ext.inters = []
    inters = sort_this(ext.gen_inters(myfun.size-1))
    cnt = myfun.size-2
    for inter in inters:
        if inter.count('u') < cnt:
            if msats:
                break
            else:
                cnt -= 1
        sat = inter[:a.dex] + 'u' + inter[a.dex:]
        if satisfies(v, sat, a):
            msats.append(sat)

    return msats


# Generates set of minimal satisfiable interpretations for argument a under interpretation v.
def msat_comp_4(v, a):
    sats = []
    ext.inters = []
    inters = ext.gen_inters(myfun.size-1)
    for inter in inters:
        sat = inter[:a.dex] + 'u' + inter[a.dex:]
        if satisfies(v, sat, a):
            sats.append(sat)

    msats = min_info(sats)
    return msats


# Generates a random interpretation over the parents of a. Not necessarily satisfiable.
def msat_random(v, a):
    sat = ''
    par_in = []

    for j, arg in enumerate(v):
        if myfun.arguments[j].sym in a.ac.atoms():
            choices = ['u', 't', 'f']
            sat = sat + random.choice(choices)
            par_in.append(j)
        else:
            sat = sat + 'u'

    return sat, par_in


# Generates a random satisfiable interpretation over the parents of a. Not necessarily minimal.
def msat_random_sat(v, a):
    while True:
        rand = msat_random(v, a)
        if satisfies(v, rand[0], a):
            break
    return rand[0]
