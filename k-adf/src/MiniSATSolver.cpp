/*!
 * Copyright (c) <2018> <Andreas Niskanen, University of Helsinki>
 * 
 * 
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * 
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * 
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "MiniSATSolver.h"

using namespace std;
using namespace Minisat;

MiniSATSolver::MiniSATSolver()
{
    n_vars = 0;
    solver = new Solver();
}

void MiniSATSolver::add_clause(vector<int> & clause)
{
    vec<Lit> lits;
    for (int i = 0; i < clause.size(); i++) {
        int var = abs(clause[i])-1;
        while (var >= solver->nVars()) {
            solver->newVar();
            n_vars++;
        }
        lits.push((clause[i] > 0) ? mkLit(var) : ~mkLit(var));
    }
    solver->addClause_(lits);
    clauses.push_back(clause);
}

void MiniSATSolver::add_clauses(vector<vector<int>> & clauses)
{
    for (int i = 0; i < clauses.size(); i++) {
        add_clause(clauses[i]);
    }
}

bool MiniSATSolver::solve()
{
    bool sat = solver->solve();
    if (sat) {
        for (int i = 0; i < solver->model.size(); i++) {
            assignment[i] = (solver->model[i] == l_True) ? 1 : 0;
        }
    }
    return sat;
}

bool MiniSATSolver::solve(vector<int> & assumptions)
{
    vec<Lit> lits;
    for (int i = 0; i < assumptions.size(); i++) {
        int var = abs(assumptions[i])-1;
        while (var >= solver->nVars()) {
            solver->newVar();
            n_vars++;
        }
        lits.push((assumptions[i] > 0) ? mkLit(var) : ~mkLit(var));
    }
    bool sat = solver->solve(lits);
    if (sat) {
        for (int i = 0; i < solver->model.size(); i++) {
            assignment[i] = (solver->model[i] == l_True) ? 1 : 0;
        }
    }
    return sat;
}
