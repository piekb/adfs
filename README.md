# adfs
Bachelor Project on Abstract Dialectical Frameworks.

# src
Source code. Main code is main.py
To compile: 
To run: python main.py
You will be asked to enter an input file name and initial claim. 

# ex
Location of example ADF input files. Format:
s(a). 		... a is an argument
ac(a,f).	... the acceptance condition of a is f, 
		    where f is a propositional formula
		    consisting of argument symbols,
		    c(v) for true, c(f) for false, 
		    neg(p), and(p,q), or(p,q), xor(p,q),
		    imp(p,q), iff(p,q), where p and q
		    are subformulae.


# k-adf
K++ ADF, for reference. Altered SolverTypes.h.
cd src
To compile: make
To run: ./k++adf <adm/prf> <options> <file>
Files are in ../ex
