## Global variables, classes, and functions

arguments = []
size = 0

## Takes expression and interpretation, and returns evaluated expression under interpretation
def phi(exp, v, args):
    new = exp
    for i, val in enumerate(v):
        if val == 't':
            new = new.subs({args[i].sym: True})
        elif val == 'f':
            new = new.subs({args[i].sym: False})

    # print(new)
    return new

## Gamma with args as objects with ac, set_args as symbols
## For whole set of arguments! So not necessarily >=i
def gamma(v, args):
    new = ''
    # print(v)
    for a in args:
        update = phi(a.ac, v, args)
        # print(update)
        if update == True:
            new = new + 't'
        elif update == False:
            new = new + 'f'
        else:
            new = new + 'u'
    # print(new)
    return new

## v(a): returns truth value of argument arg in interpretation v
def find_in(v,arg,arguments):
    return v[dexin(v, arg, arguments)]

# index() but for arguments in v
def dexin(v,arg,arguments):
    index = 0
    for i, val in enumerate(v):
        if arguments[i].name == arg.name:
            index = i

    return index

def print_full_args(set):
    for a in set:
        print(a.name)
        print(a.ac)

def print_args(set):
    for a in set:
        print(a.name)

def print_acs(set):
    for a in set:
        print(a)