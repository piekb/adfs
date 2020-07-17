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
def msat_comp_4(v, a):
    msats = []
    inters = sort_this(ext.gen_inters(myfun.size-1))
    cnt = myfun.size-2
    for inter in inters:
        if inter.count('u') < cnt:
            if msats:
                break
            else:
                # When e.g. phi(a) = b & c, just one t/f doesn't satisfy it
                cnt -= 1
        sat = inter[:a.dex] + 'u' + inter[a.dex:]
        if satisfies(v, sat, a):
            msats.append(sat)

    # msats = min_info(sats)
    return msats


# Generates set of minimal satisfiable interpretations for argument a under interpretation v.
def msat_comp_3(v, a):
    sats = []
    inters = ext.gen_inters(myfun.size-1)
    for inter in inters:
        sat = inter[:a.dex] + 'u' + inter[a.dex:]
        if satisfies(v, sat, a):
            sats.append(sat)

    msats = min_info(sats)
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


# New idea
def msat_comp_6(v, arg):
    ext.inters = []
    num_par = len(arg.ac.atoms())
    inters = ext.gen_inters(num_par)[1:]
    msats = []
    cnt = num_par - 1

    inter = random.choice(inters)
    new_inter = ''

    def find_random():
        new_inter = ''
        j = 0
        # This part is still quite slow
        for i, _ in enumerate(v):
            if myfun.arguments[i].sym in arg.ac.atoms():
                new_inter += inter[j]
                j += 1
            else:
                new_inter += 'u'

    find_random()
    while not satisfies(v, new_inter, arg):
        inter = random.choice(inters)
        find_random()
    # print(new_inter)


# New idea
def msat_comp_5(idx, v, arg):
    ext.inters = []
    num_par = len(arg.ac.atoms())
    inters = sort_this(ext.gen_inters(num_par)[1:])
    k = 0
    print("here, we have k, i = ", k, idx)
    for inter in inters:
        new_inter = ''
        j = 0
        for i, _ in enumerate(v):
            if myfun.arguments[i].sym in arg.ac.atoms():
                new_inter += inter[j]
                j += 1
            else:
                new_inter += 'u'
        if satisfies(v, new_inter, arg):
            print("k, i", k, idx)
            if k == idx:
                return new_inter
            else:
                print("k, i, new_inter", k, idx, new_inter)
                k += 1
    print("no msat found, k = ", k)
    return ''


def find_new(i, v, a_prime, choice):
    msats = {}
    for a in a_prime:
        phi_a = myfun.phi(a.ac, v)
        if phi_a == True or phi_a == False:
            # Second condition of mSAT_F; there is no other mSAT
            m = [myfun.just_one_gamma(v, a)]
            msats[f"{a.name}"] = m
        else:
            # msat_comp_6(v, a)
            # New idea
            if choice == 5:
                m = [msat_comp_5(i, v, a)]
                msats[f"{a.name}"] = m
                print(m)
            # Smart computation over all arguments
            elif choice == 4:
                msats[f"{a.name}"] = msat_comp_4(v, a)
            # Computation over all arguments
            elif choice == 3:
                msats[f"{a.name}"] = msat_comp_3(v, a)
            # Computation over parents of a in A'
            elif choice == 2:
                msats[f"{a.name}"] = msat_comp_2(v, a)
            # One SAT (not minimal) randomly generated over parents of a in A'
            elif choice == 0:
                m = [msat_smart(v, a)]
                msats[f"{a.name}"] = m
            # Smarter computation over parents of a in A'
            elif choice == 1:
                msats[f"{a.name}"] = msat_comp_1(v, a)
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
