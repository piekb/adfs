CURR_DIR   = $(shell pwd)

SAT_SOLVER = minisat

MINISAT    = $(CURR_DIR)/../minisat

CFLAGS = -std=c++11 -O3 -D __STDC_LIMIT_MACROS -D __STDC_FORMAT_MACROS -Wno-literal-suffix
OBJS = Formula.o Node.o ADF.o Utils.o Encodings.o Exists.o CredAcceptance.o SkeptAcceptance.o Enumeration.o Polarity.o Main.o

ifeq ($(SAT_SOLVER), minisat)
	SAT_DIR = $(MINISAT)
	CFLAGS += -DSAT_MINISAT -I$(MINISAT) -lz
	OBJS += MiniSATSolver.o
	SAT_OBJS = $(MINISAT)/core/Solver.o
	SOLVER = Solver.o
else
	$(error No SAT solver specified.)
endif

.cc.o:
	g++ $(CFLAGS) -c $<

.cpp.o:
	g++ $(CFLAGS) -c $<

all:    $(OBJS) $(SAT_OBJS)
	g++ $(CFLAGS) $(OBJS) $(SOLVER) -o k++adf $(LNFLAGS)

clean:
	rm *o k++adf
