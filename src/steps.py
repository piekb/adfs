import myfun
# as f
from myfun import *

def fail():
    print("information lost!")

def finish():
    print("next player")

# Check if oldv <= v between each step (so all v's are in fact comparable!)
def check_info(v,oldv,arguments):
    a_prime = []
    for i,val in enumerate(v):
        if (oldv[i] == 'u'):
            if (v[i] == 't' or v[i] == 'f'):
                a_prime.append(arguments[i])
        else:
            if (v[i] != oldv[i]):
                fail()
    if len(a_prime)==0:
        finish()

    return a_prime

    # forward(v,a_prime,args)


## Forward move
## Evaluate AC of all a in A-prime
def forward(v,a_prime,args):
    updated_acs = []
    for a in a_prime:
        updated_acs.append(myfun.eval_exp(a.ac, v, args))

    for ac in updated_acs:
        print(ac)

