from sympy import simplify

# This file contains global variables and functions used in other files.
arguments = []
size = 0
pc = False


# Check if oldv <= v between each step
def check_info(v, oldv):
    a_prime = []
    contra = False
    found = False
    for i, val in enumerate(v):
        if oldv[i] == 'u':
            if v[i] == 't' or v[i] == 'f':
                a_prime.append(arguments[i])
        else:
            if v[i] != oldv[i]:
                contra = True
    if len(a_prime) == 0:
        # Actually, not found if contradiction.
        found = True
    return a_prime, contra, found


# Returns an interpretation with only arg -> value and all other args -> u
def make_one(value, arg_name):
    u = size * 'u'
    arg_in = dex(arg_name)
    new = u[:arg_in] + value + u[arg_in:-1]
    return new


# Returns {a to Gamma(v)(a)}
def just_one_gamma(v, a):
    new = find_in(gamma(v), a)
    gam = make_one(new, a.name)
    return gam


# Takes expression and interpretation, and returns evaluated expression under interpretation
def phi(exp, v):
    if exp == True or exp == False:
        return exp
    else:
        new = exp
        for i, val in enumerate(v):
            if val == 't':
                new = new.subs({arguments[i].sym: True})
            elif val == 'f':
                new = new.subs({arguments[i].sym: False})

        return simplify(new)


# Gamma of v. Resulting interpretation of evaluating phi(a) under v
def gamma(v):
    new = ''
    for a in arguments:
        update = phi(a.ac, v)
        if update == True:
            new = new + 't'
        elif update == False:
            new = new + 'f'
        else:
            new = new + 'u'
    return new


# v(a): returns truth value of argument arg (a symbol) in any interpretation v
def find_in(v, arg):
    return v[arg.dex]


# Finds the index of an argument by name
def dex(arg_name):
    for a in arguments:
        if a.name == arg_name:
            return a.dex


# Finds argument from a symbol. Used because atoms() returns symbols
def find_from_sym(s):
    for a in arguments:
        if a.sym == s:
            return a


# Prints all arguments and their acceptance conditions in given set
def print_full_args(set):
    for a in set:
        print(f"phi({a.name}): {a.ac}")
