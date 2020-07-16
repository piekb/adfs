from typing import Dict, Any, Union
import myfun
import ext
import random

from myfun import *
from ext import *

black_list = []


def xprint(string):
    if myfun.pc:
        print(string)


def sort_this(list):
    d = dict.fromkeys(list, 1)
    for i, sat in enumerate(list):
        d[f'{sat}'] = sat.count('t') + sat.count('f')

    sort = sorted(d, key=d.get)
    # print("sorted:", sort)
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


# Generates set of minimal satisfiable interpretations for argument a under interpretation v.
# Complexity optimized by bottom-up search for minimality
def msat_comp(v, arg):
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


def find_new(v, a_prime, choice):
    msats = {}
    for a in a_prime:
        phi_a = myfun.phi(a.ac, v)
        if phi_a == True or phi_a == False:
            # Second condition of mSAT_F; there is no other mSAT
            m = [myfun.just_one_gamma(v, a)]
            msats[f"{a.name}"] = m
        else:
            # Computation over all arguments
            if choice == 2:
                msats[f"{a.name}"] = gen_msats(v, a)
            # One SAT (not minimal) randomly generated over parents of a in A'
            elif choice == 1:
                m = [msat_smart(v, a)]
                msats[f"{a.name}"] = m
            # Smarter computation over parents of a in A'
            elif choice == 0:
                msats[f"{a.name}"] = msat_comp(v, a)
    result = ext.combine_msats(msats)
    num = len(result[f"{a_prime[0].name}"])
    return num, result


# Not super low complexity I think
def minimal(v, sat, arg):
    msat = sat[0]
    par_in = sat[1]

    ext.inters = []
    inters = ext.gen_inters(len(par_in))
    # ext.allKLengthRec(['u', 't', 'f'], "", 3, len(par_in))
    op = inters[1:]
    random.shuffle(op)
    new = []
    for inter in op:
        new_m = ''
        j = 0
        for i, _ in enumerate(v):
            if i in par_in:
                new_m += inter[j]
                j += 1
            else:
                new_m += 'u'
        if satisfies(v, new_m, arg):
            new.append(new_m)

        if new_m.count('u') > msat.count('u'):
            if satisfies(v, new_m, arg):
                msat = new_m
    msats = min_info(new)

    return msats


def satisfies(v, new_v, a):
    v_a = myfun.find_in(v, a)
    gam_a = myfun.find_in(myfun.gamma(new_v), a)
    # print(f"for arg {a.name} v({a.name}) = {v_a}")
    # print(f"for arg {a.name} gamma({a.name}) = {gam_a}")
    return v_a == gam_a


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


def msat_smart(v, a):
    while True:
        rand = msat_random(v, a)
        if satisfies(v, rand[0], a):
            break
    # msats = minimal(v, rand, a)

    # return msats
    return rand[0]

# IDEA: for parents(a), find indices --> make msat with u's and rand(t,f) in those places. Try until satisfiable.
# Won't be absolutely minimal though... find all then find minimal? Not sure if still too complex
# Find random msat, but keep track of which have been used and rejected
