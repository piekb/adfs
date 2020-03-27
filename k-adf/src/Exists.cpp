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

#include <iostream>

#include "Constants.h"
#include "Encodings.h"
#include "Exists.h"
#include "Utils.h"

#if defined(SAT_MINISAT)
#include "MiniSATSolver.h"
typedef MiniSATSolver SAT_Solver;
#elif defined(SAT_GLUCOSE)
#include "GlucoseSolver.h"
typedef GlucoseSolver SAT_Solver;
#elif defined(SAT_CRYPTO)
#include "CryptoMiniSATSolver.h"
typedef CryptoMiniSATSolver SAT_Solver;
#else
#error "No SAT solver defined"
#endif


using namespace std;

namespace Exists {

vector<int> exists_cf(ADF & adf, std::vector<int> & interpretation) {
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	bool sat = solver.solve();

	vector<int> model;
	if (sat) {
		for (int i = 0; i < adf.statements.size(); i++) {
			if (solver.assignment[adf.statement_true_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::True);
			} else if (solver.assignment[adf.statement_false_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::False);
			} else {
				model.push_back(Interpretation::Undefined);
			}
		}
	}
	return model;
}

vector<int> exists_adm(ADF & adf, std::vector<int> & interpretation) {
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	vector<int> model;
	model.resize(adf.statements.size());
	while (true) {
		bool sat = solver.solve();
		if (!sat) break;
		for (int i = 0; i < adf.statements.size(); i++) {
			if (solver.assignment[adf.statement_true_var[adf.statements[i]]-1]) {
				model[i] = Interpretation::True;
			} else if (solver.assignment[adf.statement_false_var[adf.statements[i]]-1]) {
				model[i] = Interpretation::False;
			} else {
				model[i] = Interpretation::Undefined;
			}
		}
		SAT_Solver new_solver = SAT_Solver();
		vector<vector<int>> adm_clauses = adm_verification(adf, model);
		new_solver.add_clauses(adm_clauses);
		if (new_solver.solve()) {
			vector<int> refinement_clause;
			for (int i = 0; i < adf.statements.size(); i++) {
				if (model[i] == Interpretation::True) {
					refinement_clause.push_back(-adf.statement_true_var[adf.statements[i]]);
				} else if (model[i] == Interpretation::False) {
					refinement_clause.push_back(-adf.statement_false_var[adf.statements[i]]);
				} else {
					refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
					refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
				}
			}
			solver.add_clause(refinement_clause);
		} else {
			return model;
		}
	}
	vector<int> empty_model;
	return empty_model;
}

vector<int> exists_adm_bipolar(ADF & adf, std::vector<int> & interpretation) {
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	bool sat = solver.solve();

	vector<int> model;
	if (sat) {
		for (int i = 0; i < adf.statements.size(); i++) {
			if (solver.assignment[adf.statement_true_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::True);
			} else if (solver.assignment[adf.statement_false_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::False);
			} else {
				model.push_back(Interpretation::Undefined);
			}
		}
	}
	return model;
}

vector<int> exists_adm_k_bipolar(ADF & adf, std::vector<int> & interpretation) {
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> k_bipolar_clauses = k_bipolar_interpretation(adf, interpretation);
	solver.add_clauses(k_bipolar_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	bool sat = solver.solve();

	vector<int> model;
	if (sat) {
		for (int i = 0; i < adf.statements.size(); i++) {
			if (solver.assignment[adf.statement_true_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::True);
			} else if (solver.assignment[adf.statement_false_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::False);
			} else {
				model.push_back(Interpretation::Undefined);
			}
		}
	}
	return model;
}

vector<int> exists_grd(ADF & adf) {
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> base_clauses;
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	base_clauses.push_back(true_clause);
	base_clauses.push_back(false_clause);
	while (true) {
		vector<int> new_interpretation;
		for (int i = 0; i < adf.statements.size(); i++) {
			SAT_Solver solver = SAT_Solver();
			solver.add_clauses(base_clauses);
			solver.add_clauses(adf.statement_clauses[i]);
			for (int j = 0; j < interpretation.size(); j++) {
				if (interpretation[j] == Interpretation::True) {
					vector<int> clause;
					clause.push_back(adf.statement_var[adf.statements[j]]);
					solver.add_clause(clause);
				} else if (interpretation[j] == Interpretation::False) {
					vector<int> clause;
					clause.push_back(-adf.statement_var[adf.statements[j]]);
					solver.add_clause(clause);
				}
			}
			int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->global_value;
			vector<int> not_tautology_clause = {-val};
			vector<int> not_unsat_clause = {val};
			bool not_tautology = solver.solve(not_tautology_clause);
			bool not_unsat = solver.solve(not_unsat_clause);
			if (!not_tautology) {
				new_interpretation.push_back(Interpretation::True);
			} else if (!not_unsat) {
				new_interpretation.push_back(Interpretation::False);
			} else {
				new_interpretation.push_back(Interpretation::Undefined);
			}
		}
		bool fixpoint = true;
		for (int i = 0; i < interpretation.size(); i++) {
			if (interpretation[i] != new_interpretation[i]) {
				fixpoint = false;
				break;
			}
		}
		if (fixpoint) {
			break;
		} else {
			interpretation = new_interpretation;
		}
	}
	return interpretation;
}

}
