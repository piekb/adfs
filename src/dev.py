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

## == c with ac = b | ~a
# testarg = arguments[2]
# print(testarg.name)
# print(testarg.ac)
# print("now removed:")
# try:
#     test = arguments
#     test.remove(testarg)
#     myfun.print_full_args(test)
# except ValueError:
#     print("Given argument does not exist")

## Returns a version of a-prime without the "current" argument, to avoid double checking
# def exclude(a_prime, a):
#     try:
#         rest_a_prime = a_prime
#         rest_a_prime.remove(a)
#         return rest_a_prime
#     except ValueError:
#         print("Given argument does not exist")


## Find one mSAT for one argument
# def give_msat(a):
#     msat = ''
#     if '{}'.format(a) in known_msats.keys():
#         msat = known_msats['{}'.format(a)]
#     else:
#         msat = input(
#             "Please give an msat w for arg {arg} with condition = {ac} such that gamma(w)({arg}) = v({arg}): ".format(
#                 arg=a.name, ac=a.ac))
#         while True:
#             if re.match("^[f,t,u]*$", msat) and len(
#                     msat) == myfun.size:  # and myfun.find_in(v, a, arguments) == myfun.find_in(gamma(v, arguments), a, arguments)
#                 known_msats['{}'.format(a)] = msat
#                 break
#             else:
#                 print("Error! Input should be {size} characters from t,f, or u. No spaces".format(size=myfun.size))
#                 msat = input(
#                     "Please give an msat w for arg {arg} with condition = {ac} such that gamma(w)({arg}) = v({arg}): ".format(
#                         arg=a.name, ac=a.ac))
#
#     return msat
