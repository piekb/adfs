## Takes expression and interpretation, and returns evaluated expression under interpretation
def eval_exp(exp, v, args):
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
def gamma(v,args):
    new = ''
    print(v)
    for a in args:
        update = eval_exp(a.ac, v, args)
        print(update)
        if update == True:
            new = new + 't'
        elif update == False:
            new = new + 'f'
        else:
            new = new + 'u'
    print(new)
    # return new

def print_full_args(set):
    for a in set:
        print(a.name)
        print(a.ac)

def print_args(set):
    for a in set:
        print(a.name)
