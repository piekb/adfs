from sympy import simplify

## Global variables, classes, and functions
arguments = []
size = 0

# Check if oldv <= v between each step
def check_info(v, oldv):
    a_prime = []
    contra = False
    found = False
    for i, val in enumerate(v):
        if oldv[i] == 'u':
            if v[i] == 't' or v[i] == 'f':
                print(f'adding {arguments[i].name} to aprime')
                a_prime.append(arguments[i])
        else:
            if v[i] != oldv[i]:
                print("contradiction found!")
                contra = True
    if len(a_prime) == 0:
        # Actually, not found if contradiction. But adding not contra gives
        found = True
    return a_prime, contra, found


# Returns an interpretation with only arg -> value, and all other args -> u
def make_one(value, arg):
    u = size * 'u'
    arg_in = dex(arg)
    new = u[:arg_in] + value + u[arg_in:-1]

    return new


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

        # print(new)
        # print(f'this is {simplify(new)}')
        return simplify(new)


# Gamma with args as objects with ac, set_args as symbols
# For whole set of arguments! So not necessarily >=i
def gamma(v):
    new = ''
    # print(v)
    for a in arguments:
        update = phi(a.ac, v)
        # print(update)
        if update == True:
            new = new + 't'
        elif update == False:
            new = new + 'f'
        else:
            new = new + 'u'
    # print(new)
    return new


# v(a): returns truth value of argument arg in interpretation v
def find_in(v, arg):
    return v[dex(arg.name)]


# Finds the index of an argument by name
def dex(arg_name):
    for a in arguments:
        if a.name == arg_name:
            return a.dex


def print_full_args(set):
    for a in set:
        print(a.name, ":", a.ac)


def print_args(set):
    for a in set:
        print(a.name)


def print_acs(set):
    for a in set:
        print(a)
