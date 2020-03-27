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

#include "SkeptAcceptance.h"
#include "Constants.h"
#include "Encodings.h"
#include "CredAcceptance.h"
#include "Exists.h"

#if defined(SAT_MINISAT)
#include "MiniSATSolver.h"
typedef MiniSATSolver SAT_Solver;
#else
#error "No SAT solver defined"
#endif

using namespace std;

namespace SkeptAcceptance {

bool skept_nai(ADF & adf, int statement) {
	if (adf.opt) {
		if (!CredAcceptance::cred_cf(adf, statement)) {
			return false;
		}
	}
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	while (true) {
		bool sat = solver.solve();
		if (!sat) {
			return true;
		}
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
		new_solver.add_clauses(cf_clauses);
		while (true) {
			vector<vector<int>> larger_clauses_ = larger_interpretation(adf, model);
			new_solver.add_clauses(larger_clauses_);
			bool sat = new_solver.solve();
			if (!sat) break;
			for (int i = 0; i < adf.statements.size(); i++) {
				if (new_solver.assignment[adf.statement_true_var[adf.statements[i]]-1]) {
					model[i] = Interpretation::True;
				} else if (new_solver.assignment[adf.statement_false_var[adf.statements[i]]-1]) {
					model[i] = Interpretation::False;
				} else {
					model[i] = Interpretation::Undefined;
				}
			}
		}
		if (model[statement-1] != Interpretation::True) {
			return false;
		}
		vector<int> refinement_clause;
		for (int i = 0; i < adf.statements.size(); i++) {
			if (model[i] == Interpretation::True) {
				refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
			} else if (model[i] == Interpretation::False) {
				refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
			} else {
				refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
				refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
			}
		}
		solver.add_clause(refinement_clause);
	}
}

bool skept_prf(ADF & adf, int statement) {
	SAT_Solver solver = SAT_Solver();
	if (adf.opt) {
	if (!CredAcceptance::cred_adm(adf, statement)) {
		return false;
	}
	vector<int> grounded = Exists::exists_grd(adf);
	if (grounded[statement-1] == Interpretation::True) {
		return true;
	} else if (grounded[statement-1] == Interpretation::False) {
		return false;
	}
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, grounded);
	solver.add_clauses(larger_clauses);
	} else {
	vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	}
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
			while (true) {
				vector<int> new_model = Exists::exists_adm(adf, model);
				if (new_model.size() != 0) {
					model = new_model;
				} else {
					break;
				}
			}
			if (model[statement-1] != Interpretation::True) {
				return false;
			}
			vector<int> refinement_clause;
			for (int i = 0; i < adf.statements.size(); i++) {
				if (model[i] == Interpretation::True) {
					refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
				} else if (model[i] == Interpretation::False) {
					refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
				} else {
					refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
					refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
				}
			}
			solver.add_clause(refinement_clause);
		}
	}
	return true;
}

bool skept_prf_bipolar(ADF & adf, int statement) {
	SAT_Solver solver = SAT_Solver();
	if (adf.opt) {
	if (!CredAcceptance::cred_adm_bipolar(adf, statement)) {
		return false;
	}
	vector<int> grounded = Exists::exists_grd(adf);
	if (grounded[statement-1] == Interpretation::True) {
		return true;
	} else if (grounded[statement-1] == Interpretation::False) {
		return false;
	}
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, grounded);
	solver.add_clauses(larger_clauses);
	} else {
	vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	}
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
		while (true) {
			vector<int> new_model = Exists::exists_adm_bipolar(adf, model);
			if (new_model.size() != 0) {
				model = new_model;
			} else {
				break;
			}
		}
		if (model[statement-1] != Interpretation::True) {
			return false;
		}
		vector<int> refinement_clause;
		for (int i = 0; i < adf.statements.size(); i++) {
			if (model[i] == Interpretation::True) {
				refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
			} else if (model[i] == Interpretation::False) {
				refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
			} else {
				refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
				refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
			}
		}
		solver.add_clause(refinement_clause);
	}
	return true;
}

bool skept_prf_k_bipolar(ADF & adf, int statement) {
	SAT_Solver solver = SAT_Solver();
	if (adf.opt) {
	if (!CredAcceptance::cred_adm_k_bipolar(adf, statement)) {
		return false;
	}
	vector<int> grounded = Exists::exists_grd(adf);
	if (grounded[statement-1] == Interpretation::True) {
		return true;
	} else if (grounded[statement-1] == Interpretation::False) {
		return false;
	}
	vector<vector<int>> k_bipolar_clauses = k_bipolar_interpretation(adf, grounded);
	solver.add_clauses(k_bipolar_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, grounded);
	solver.add_clauses(larger_clauses);
	} else {
	vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> k_bipolar_clauses = k_bipolar_interpretation(adf, interpretation);
	solver.add_clauses(k_bipolar_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	}
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
		while (true) {
			vector<int> new_model = Exists::exists_adm_k_bipolar(adf, model);
			if (new_model.size() != 0) {
				model = new_model;
			} else {
				break;
			}
		}
		if (model[statement-1] != Interpretation::True) {
			return false;
		}
		vector<int> refinement_clause;
		for (int i = 0; i < adf.statements.size(); i++) {
			if (model[i] == Interpretation::True) {
				refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
			} else if (model[i] == Interpretation::False) {
				refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
			} else {
				refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
				refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
			}
		}
		solver.add_clause(refinement_clause);
	}
	return true;
}

}
