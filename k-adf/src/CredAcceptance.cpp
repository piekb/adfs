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

#include "CredAcceptance.h"
#include "Constants.h"
#include "Encodings.h"

#if defined(SAT_MINISAT)
#include "MiniSATSolver.h"
typedef MiniSATSolver SAT_Solver;
#else
#error "No SAT solver defined"
#endif

using namespace std;

namespace CredAcceptance {

bool cred_cf(ADF & adf, int statement) {
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	vector<int> statement_true_clause = {adf.statement_true_var[statement]};
	solver.add_clause(statement_true_clause);
	bool sat = solver.solve();
	return sat;
}

bool cred_adm(ADF & adf, int statement) {
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	vector<int> statement_true_clause = {adf.statement_true_var[statement]};
	solver.add_clause(statement_true_clause);
	while (true) {
		bool sat = solver.solve();
		if (!sat) break;
		vector<int> model;
		for (int i = 0; i < adf.statements.size(); i++) {
			if (solver.assignment[adf.statement_true_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::True);
			} else if (solver.assignment[adf.statement_false_var[adf.statements[i]]-1]) {
				model.push_back(Interpretation::False);
			} else {
				model.push_back(Interpretation::Undefined);
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
			return true;
		}
	}
	return false;
}

bool cred_adm_bipolar(ADF & adf, int statement) {
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	vector<int> statement_true_clause = {adf.statement_true_var[statement]};
	solver.add_clause(statement_true_clause);
	bool sat = solver.solve();
	return sat;
}

bool cred_adm_k_bipolar(ADF & adf, int statement) {
	SAT_Solver solver = SAT_Solver();
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> k_bipolar_clauses = k_bipolar_interpretation(adf, interpretation);
	solver.add_clauses(k_bipolar_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	vector<int> statement_true_clause = {adf.statement_true_var[statement]};
	solver.add_clause(statement_true_clause);
	bool sat = solver.solve();
	return sat;
}

}