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

## Returns the set of mSAT interpretations from a list of SAT interpretations.
def min_info(sats):
    msats = []
    d = dict.fromkeys(sats, 1)
    for i, sat in enumerate(sats):
        count = 0
        for j, tv in enumerate(sat):
            if tv != 'u':
                count += 1
        d['{}'.format(sat)] = count

    sort = sorted(d, key=d.get)
    # last = sort[0]
    for w in sort:
        # print(w, d[w])
        if d[w] == d[sort[0]]:
            msats.append(w)

    return msats

## Generates set of minimal satisfiable interpretations for argument a under interpretation v.
def gen_msats(a, v, arguments):
    inters = ext.gen_inters(myfun.size)
    # print('before:')
    sats = []
    arg_in = myfun.dexin(v, a, arguments)

    for i, inter in enumerate(inters):
        sat = inter[:arg_in] + 'u' + inter[arg_in:]
        v_a = myfun.find_in(v, a, arguments)
        gam_a = myfun.find_in(myfun.gamma(sat, arguments), a, arguments)
        # print("for arg {arg} v({arg}) = {v}".format(arg = a.name, v = v_a))
        # print("for arg {arg} gamma({arg}) = {v}".format(arg=a.name, v=gam_a))
        if v_a == gam_a:
            sats.append(sat)
    # print(sats)

    msats = min_info(sats)
    # print(msats)
    return msats

def find_msat(a, v, args):
    phi_a = myfun.phi(a.ac, v, args)
    if '{}'.format(a) in known_msats.keys():
        msat = known_msats['{}'.format(a)]
    else:
        msats = gen_msats(a, v, args)
        if phi_a == True or phi_a == False or len(msats) == 0:
            print("here now")
            msat = just_one_gamma(v, a, args)
        else:
            msat = msats[0]
        known_msats['{}'.format(a)] = msat
    # print('msat for arg {a} = {msat}'.format(a=a.name, msat=msat))
    return msat

## Returns if there is any conflict in the "rest" of a-prime without the first defined value.
## Check if msatai!=msataj also a problem if msataj == u?
def no_conflict(a_prime, v, arg, arguments):
    val_ai = myfun.find_in(v, arg, arguments)
    for a in a_prime:
        msat_aj = find_msat(a, v, arguments)
        val_aj = myfun.find_in(msat_aj, arg, arguments)
        if val_aj != 'u' and val_ai != 'u' and val_aj != val_ai:
            print('here is conflict: val_ai = {ai}, val_aj={aj} for arg {arg} on arg {a}'.format(ai=val_ai, aj=val_aj, arg=arg.name, a=a.name))
            return False

    return True


## Returns {a to Gamma(v)(a)}
def just_one_gamma(v, arg, arguments):
    u = myfun.size * 'u'

    new = myfun.find_in(myfun.gamma(v, arguments), arg, arguments)
    # print('new = {}'.format(new))

    arg_in = myfun.dexin(v, arg, arguments)
    msat = u[:arg_in] + new + u[arg_in:-1]
    # if msat.count('u') == myfun.size:
    #     print("help me please")
    return msat

def third(arg, v, arguments, a_prime):
    phi_a = myfun.phi(arg.ac, v, arguments)
    print('third condition')
    msat_arg = find_msat(arg, v, arguments)
    if msat_arg == just_one_gamma(v, arg, arguments):
        return False
    else:
        for c in phi_a.atoms():
            # val_a_c = myfun.find_in(msat_arg, c, arguments)
            if not no_conflict(a_prime, v, c, arguments):
                print("- conflict found -")
                return False
    return True


def fourth(a_prime, v, arg, arguments):
    print('fourth condition')
    for a in a_prime:
        msat_ai = find_msat(a, v, arguments)
        print("msat for {a} is: {msat}".format(a=a.name, msat=msat_ai))
        # print(msat_ai)
        val = myfun.find_in(msat_ai, arg, arguments)

        ## Clean up, now there's a double finding val in v
        if val == 't' or val == 'f':
            if no_conflict(a_prime, v, arg, arguments):
                return True, msat_ai
    return False, 0


def delta(v, a_prime, arg, arguments):
    # print("for arg {}".format(arg.name))
    update = ''
    truth_val = myfun.find_in(v, arg, arguments)
    if truth_val == 't' or truth_val == 'f':
        if not (arg in a_prime):
            print("first case in delta")
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
    # myfun.print_acs(updated_acs)

    out = ''
    for a in args:
        out = out + delta(v, a_prime, a, args)

    print("final delta:")
    print(out)
    return out
