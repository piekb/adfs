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
m_a = ['tfu']
m_b = ['tuf', 'ttt', 'fff']
m_c = ['ftt', 'tfu']

m_all = [['tfu', 'tuf', 'ftt'],
         ['tfu', 'ttt', 'ftt'],
         ['tfu', 'fff', 'ftt'],
         ['tfu', 'tuf', 'tfu'],
         ['tfu', 'ttt', 'tfu'],
         ['tfu', 'fff', 'tfu']]
full = []


def combine():
    full.append()


def combine():
    for e in m_a:
        for f in m_b:
            for g in m_c:
                full.append([e, f, g])

    print(full)


# def find_msat(v, a):
    # phi_a = myfun.phi(a.ac, v)
    # if f'{a.name}' in msats.keys():
    #     msat = msats[f'{a.name}'][i]
    #     if len(msats[f'{a.name}']) <= i:
    #         print("Hey, that doesn't exist!")
            # print(f"heya, msat for {a.name} is {msats[f'{a.name}'][i]}")
            # msat = msats[f'{a.name}'][0]
        # else:
        #     print("i = 0 hoor rustig maar tijger")
        #     print(f"heya, msat for {a.name} is {msats[f'{a.name}'][0]}")

    # if f'{a}' in known_msats.keys():
    #     msat = known_msats[f'{a}']
    # else:
    #     min_sats = gen_msats(v, a)
    #     if phi_a == True or phi_a == False or len(min_sats) == 0:
    # Second condition of mSAT_F
    # msat = just_one_gamma(v, a)
    # else:
    #     if len(min_sats) > i:
    #         print(f"hey, i = {i}, m = {min_sats[i]}")
    # msat = min_sats[i]
    # else:
    #     print("wuh oh")
    #     msat = min_sats[0]
    # known_msats[f'{a}'] = msat

    # return msat

# Forward move
# def forward_step(v, a_prime):
#     deltas = []
#     while i < num:
#         out = ''
#         for a in myfun.arguments:
#             print(f"Delta of argument {a.name}")
#             out = out + delta(v, a_prime, a)
#         deltas.append(out)
#         i += 1
#
#     out = ''
#     for a in myfun.arguments:
#         print(f"Delta of argument {a.name}")
#         out = out + delta(v, a_prime, a)
#     print(deltas)
#     print("Final delta:")
#     out = deltas[0]
#     print(out)
#     return deltas

# def rewrite(ac):
#     iff = ac.replace('iff', 'Equivalent').replace('imp', 'Implies').replace('neg', 'Not')
#     tf = iff.replace('and', 'And').replace('or', 'Or').replace('c(v)', 'True').replace('c(f)', 'False')
#     new = ''
#     argu = ''
#     start = False
    # for i in tf:
    #     if not start:
    #         new = new + i
    #     else:
    #         argu = argu + i
    #
    #     if i == '(':
    #         start = True
    #         # new = new + i
    #     elif i == ')':
    #         new = new + sympy.symbols(argu) + i
    #         argu = ''
    #         start = False
    #     elif i == ',':
    #         new = new + sympy.symbols(argu) + i
    #         argu = ''
    #
    #     else:





        # if i != '(' and i != ')' and i != ',':
        #     try:
        #         new = new + sympify(i)
        #     except TypeError:
                # new = new + sympify('Not(Not(i))')
                # print("hello")
                # print("type of", i, "is", type(i))
                # j = 1
                # new = new + i
        # else:
        #     new = new + i
        # print(i, type(i))
        # if type(i) is not str:
        #     print(type(i))
    # print(tf)
    # x = sympy.symbols('3')
    # print("here")
    # print(simplify(f"Or(a,3)"))
    # # print(Not(Not(tf)))
    # print(new)
    # print("done")

    # There might be a better way to convert a string to a formula, but for now this works.
    # try:
    #     simplify(tf)
    # except TypeError as error:
    #     print(type(tf))
    # s = simplify(tf)
    # print(s)
    # return simplify(tf)
    # return new