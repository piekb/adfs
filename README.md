# adfs
Bachelor Project on Abstract Dialectical Frameworks.

# src
Source code. Make sure you are in this folder! Otherwise you cannot run. 
To run: python main.py
You will be asked to enter an input file name and initial claim. 

- main.py: main script. Reads input, then runs general algorithm of the game. 
- tree.py: Tree structure functions.
- myfun.py: Functions that are used in a variety of other scripts
- msat_fun.py: Functions relating to finding mSATs. 
- forward.py: Functions relating to the forward move. 
- ext.py: Some functions I got from the internet, used for development. 
	  Two functions are actually used in the code; I will probably move those to myfun.py later. 
- dev.py: Some commented out parts of code used for development only. 
	  Just for a back-up in between Git pushes. 

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
