# adfs
Bachelor Project on Discussion Game for Abstract Dialectical Frameworks.

# requirements.txt
Installs all required packages for you. Run the following in folder 'adfs':
pip install -r requirements.txt

# src
Source code. Make sure you are in this folder! Otherwise you cannot run. 

To run: python main.py <file> <arg> <value> <algorithm> p
- file: should be the name of a file in folder "ex". 
- arg: name of argument of initial claim, for example
- value: truth value of argument in initial claim
- algorithm: 1 is smart computation over parents, 2 is normal computation over parents
- p (OPTIONAL): print steps of the game, search tree, and winning interpretation. 

Examples (used in the thesis for testing):
python main.py adfex14 a t 1
python main.py adfex7 c t 1 -p


Files:
- main.py: main script. Reads input, then runs general algorithm of the game. 
- tree.py: Tree structure functions.
- myfun.py: Functions that are used in a variety of other scripts
- msat_fun.py: Functions relating to finding mSATs. 
- forward.py: Functions relating to the forward move. 
- ext.py: Some recursive functions used by functions in msat_fun.py. 

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

The last line of the file should be empty. 
Argument names cannot start with an integer, but adding an "a" before each integer solves the problem. 
