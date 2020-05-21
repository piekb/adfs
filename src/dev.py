## Some old functions I've explored during development

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


# def reg():
# test = 'not(and(a,b))'
# pat = 'not\((.+)\)'
# found = re.match(pat,test)
# comp = re.compile(pat)
# sub = comp.search(test)
# print(sub.group(1))

# if found:
#     print("yay!")

# print(Not(And(x,a)))