# ADF (a,b),(b,or(neg(a),c)),(c,top) is counterexample :(
    # def informational(v, oldv,arguments):
    #     a_prime = []
    #     if (oldv.count("t") <= v.count("t") and oldv.count("f") <= v.count("t")):
    #         for i in enumerate(v):
    #             if (oldv[i] == 'u'):
    #                 if (v[i] == 't' or v[i] == 'f'):
    #                     a_prime.append(arguments[i])
    #         return a_prime
    #     else:
            # Found contradiction!
    # fail()

def fail():
    return False

def finish():
    return True

# Check if oldv <= v between each step (so all v's are in fact comparable!)
def check_info(v,oldv,arguments):
    a_prime = []
    for i in enumerate(v):
        if (oldv[i] == 'u'):
            if (v[i] == 't' or v[i] == 'f'):
                a_prime.append(arguments[i])
        else:
            if (v[i] != oldv[i]):
                fail()
    if len(a_prime)==0:
        finish()

    return a_prime
