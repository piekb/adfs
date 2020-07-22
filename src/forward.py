import sympy
from sympy import *
import myfun
from myfun import *
from ext import *

msat = {}


def find_msat(a):
    return msat[f"{a.name}"]


# Returns whether there is any conflict in the "rest" of a-prime
# without the first defined value. a is of class Argument
def no_conflict(val_ai, a_prime, a):
    for a_j in a_prime:
        msat_aj = find_msat(a_j)
        val_aj = myfun.find_in(msat_aj, a)
        if val_aj != 'u' and val_ai != 'u' and val_aj != val_ai:
            return False
    return True


# Third case of delta
def third(v, a_prime, a):
    phi_a = myfun.phi(a.ac, v)
    msat_arg = find_msat(a)
    if msat_arg == myfun.just_one_gamma(v, a):
        return False
    else:
        for c in phi_a.atoms():
            parent = myfun.find_from_sym(c)
            val = myfun.find_in(msat_arg, parent)
            if not no_conflict(val, a_prime, parent):
                return False
    return True


# Fourth case of delta(v, mSAT_A')(a)
def fourth(a_prime, a):
    for a_i in a_prime:
        msat_ai = find_msat(a_i)
        val = myfun.find_in(msat_ai, a)

        if val == 't' or val == 'f':
            if no_conflict(val, a_prime, a):
                return True, msat_ai
    return False, 0


# Main function delta of the forward move.
def delta(v, a_prime, a):
    update = ''
    truth_val = myfun.find_in(v, a)
    if truth_val == 't' or truth_val == 'f':
        if not (a in a_prime):
            # First case of delta
            update = truth_val
        elif (myfun.phi(a.ac, v) == True and truth_val == 't') or \
                (myfun.phi(a.ac, v) == False and truth_val == 'f'):
            # Second case of delta
            update = truth_val
        elif third(v, a_prime, a):
            # Third case of delta
            update = truth_val
        else:
            # Fifth case of delta
            update = 'u'
    elif truth_val == 'u':
        four = fourth(a_prime, a)
        if four[0]:
            # Fourth case of delta
            msat_f = four[1]
            update = myfun.find_in(msat_f, a)
        else:
            # Fifth case of delta
            update = 'u'

    return update


# Forward move
def forward_step(v, a_prime):
    out = ''
    for a in myfun.arguments:
        out = out + delta(v, a_prime, a)
    return out
