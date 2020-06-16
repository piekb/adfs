import myfun
import ext

from myfun import *
from ext import *


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


def find_new(i, v, a_prime):
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


def find_new_m(i, v, a_prime):
    new_msat = {}
    for a in a_prime:
        q = f"\t Please give mSAT option {i+1} for phi({a.name}) under {v}: "
        if i > 0:
            q = f"\t \t Please give mSAT option {i + 1} for phi({a.name}) under {v}: "
        new_msat[f'{a.name}'] = input(q)

    for a in a_prime:
        if len(new_msat[f'{a.name}']) == 0:
            return {}

    return new_msat


# IDEA: for parents(a), find indices --> make msat with u's and rand(t,f) in those places. Try until satisfiable.
# Won't be absolutely minimal though... find all then find minimal? Not sure if still too complex
