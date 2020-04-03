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

#include "Enumeration.h"
#include "Constants.h"
#include "Encodings.h"
#include "Exists.h"
#include "Utils.h"
#include <iostream>

#if defined(SAT_MINISAT)
#include "MiniSATSolver.h"
typedef MiniSATSolver SAT_Solver;
#else
#error "No SAT solver defined"
#endif

using namespace std;

namespace Enumeration {

std::vector<std::vector<int>> enumerate_cf(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	interpretations.push_back(interpretation);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
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
		interpretations.push_back(model);
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
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_nai(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
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
		interpretations.push_back(model);
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
	if (interpretations.size() == 0) {
		interpretations.push_back(interpretation);
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_adm(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	interpretations.push_back(interpretation);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	print_clauses(larger_clauses);
	while (true) {
		std::cout << "hello";
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

		print_interpretation(adf,model);
		std::cout << "-----";
		SAT_Solver new_solver = SAT_Solver();
		vector<vector<int>> adm_clauses = adm_verification(adf, model);
		new_solver.add_clauses(adm_clauses);
		if (!new_solver.solve()) {
			interpretations.push_back(model);
		}
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
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_com(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	interpretations.push_back(interpretation);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
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
		if (!new_solver.solve()) {
			vector<vector<int>> base_clauses;
			vector<int> true_clause = {adf.true_var};
			vector<int> false_clause = {-adf.false_var};
			base_clauses.push_back(true_clause);
			base_clauses.push_back(false_clause);
			while (true) {
				vector<int> new_model;
				for (int i = 0; i < adf.statements.size(); i++) {
					SAT_Solver yet_another_solver = SAT_Solver();
					yet_another_solver.add_clauses(base_clauses);
					yet_another_solver.add_clauses(adf.statement_clauses[i]);
					for (int j = 0; j < model.size(); j++) {
						if (model[j] == Interpretation::True) {
							vector<int> clause;
							clause.push_back(adf.statement_var[adf.statements[j]]);
							yet_another_solver.add_clause(clause);
						} else if (model[j] == Interpretation::False) {
							vector<int> clause;
							clause.push_back(-adf.statement_var[adf.statements[j]]);
							yet_another_solver.add_clause(clause);
						}
					}
					int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->global_value;
					vector<int> not_tautology_clause = {-val};
					vector<int> not_unsat_clause = {val};
					bool not_tautology = yet_another_solver.solve(not_tautology_clause);
					bool not_unsat = yet_another_solver.solve(not_unsat_clause);
					if (!not_tautology) {
						new_model.push_back(Interpretation::True);
					} else if (!not_unsat) {
						new_model.push_back(Interpretation::False);
					} else {
						new_model.push_back(Interpretation::Undefined);
					}
				}
				bool fixpoint = true;
				for (int i = 0; i < model.size(); i++) {
					if (model[i] != new_model[i]) {
						fixpoint = false;
						break;
					}
				}
				if (fixpoint) {
					break;
				} else {
					model = new_model;
				}
			}
			interpretations.push_back(model);
		}
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
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_prf(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
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
			interpretations.push_back(model);
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
	if (interpretations.size() == 0) {
		interpretations.push_back(interpretation);
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_adm_bipolar(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	interpretations.push_back(interpretation);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
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
		interpretations.push_back(model);
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
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_com_bipolar(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> cf_clauses = cf_interpretation(adf);
	solver.add_clauses(cf_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<int> interpretation = Exists::exists_grd(adf);
	interpretations.push_back(interpretation);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	vector<vector<int>> base_clauses;
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	base_clauses.push_back(true_clause);
	base_clauses.push_back(false_clause);
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
		while (true) {
			vector<int> new_model;
			for (int i = 0; i < adf.statements.size(); i++) {
				SAT_Solver yet_another_solver = SAT_Solver();
				yet_another_solver.add_clauses(base_clauses);
				yet_another_solver.add_clauses(adf.statement_clauses[i]);
				for (int j = 0; j < model.size(); j++) {
					if (model[j] == Interpretation::True) {
						vector<int> clause;
						clause.push_back(adf.statement_var[adf.statements[j]]);
						yet_another_solver.add_clause(clause);
					} else if (model[j] == Interpretation::False) {
						vector<int> clause;
						clause.push_back(-adf.statement_var[adf.statements[j]]);
						yet_another_solver.add_clause(clause);
					}
				}
				int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->global_value;
				vector<int> not_tautology_clause = {-val};
				vector<int> not_unsat_clause = {val};
				//print_clauses(yet_another_solver.clauses);
				bool not_tautology = yet_another_solver.solve(not_tautology_clause);
				bool not_unsat = yet_another_solver.solve(not_unsat_clause);
				if (!not_tautology) {
					new_model.push_back(Interpretation::True);
				} else if (!not_unsat) {
					new_model.push_back(Interpretation::False);
				} else {
					new_model.push_back(Interpretation::Undefined);
				}
			}
			bool fixpoint = true;
			for (int i = 0; i < model.size(); i++) {
				if (model[i] != new_model[i]) {
					fixpoint = false;
					break;
				}
			}
			refinement_clause.clear();
			for (int i = 0; i < adf.statements.size(); i++) {
				if (new_model[i] == Interpretation::True) {
					refinement_clause.push_back(-adf.statement_true_var[adf.statements[i]]);
				} else if (new_model[i] == Interpretation::False) {
					refinement_clause.push_back(-adf.statement_false_var[adf.statements[i]]);
				} else {
					refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
					refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
				}
			}
			solver.add_clause(refinement_clause);
			if (fixpoint) {
				break;
			} else {
				model = new_model;
			}
		}
		interpretations.push_back(model);
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_prf_bipolar(ADF & adf) {
	vector<vector<int>> interpretations;
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
		interpretations.push_back(model);
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
	if (interpretations.size() == 0) {
		interpretations.push_back(interpretation);
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_adm_k_bipolar(ADF & adf) {
	vector<vector<int>> interpretations;
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	interpretations.push_back(interpretation);
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> kbip_clauses = k_bipolar_interpretation(adf, interpretation);
	solver.add_clauses(kbip_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
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
		interpretations.push_back(model);
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
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_com_k_bipolar(ADF & adf) {
	vector<vector<int>> interpretations;
	SAT_Solver solver = SAT_Solver();
	vector<int> interpretation = Exists::exists_grd(adf);
	interpretations.push_back(interpretation);
	vector<vector<int>> kbip_clauses = k_bipolar_interpretation(adf, interpretation);
	solver.add_clauses(kbip_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	vector<vector<int>> base_clauses;
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	base_clauses.push_back(true_clause);
	base_clauses.push_back(false_clause);
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
		while (true) {
			vector<int> new_model;
			for (int i = 0; i < adf.statements.size(); i++) {
				SAT_Solver yet_another_solver = SAT_Solver();
				yet_another_solver.add_clauses(base_clauses);
				yet_another_solver.add_clauses(adf.statement_clauses[i]);
				for (int j = 0; j < model.size(); j++) {
					if (model[j] == Interpretation::True) {
						vector<int> clause;
						clause.push_back(adf.statement_var[adf.statements[j]]);
						yet_another_solver.add_clause(clause);
					} else if (model[j] == Interpretation::False) {
						vector<int> clause;
						clause.push_back(-adf.statement_var[adf.statements[j]]);
						yet_another_solver.add_clause(clause);
					}
				}
				int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->global_value;
				vector<int> not_tautology_clause = {-val};
				vector<int> not_unsat_clause = {val};
				bool not_tautology = yet_another_solver.solve(not_tautology_clause);
				bool not_unsat = yet_another_solver.solve(not_unsat_clause);
				if (!not_tautology) {
					new_model.push_back(Interpretation::True);
				} else if (!not_unsat) {
					new_model.push_back(Interpretation::False);
				} else {
					new_model.push_back(Interpretation::Undefined);
				}
			}
			bool fixpoint = true;
			for (int i = 0; i < model.size(); i++) {
				if (model[i] != new_model[i]) {
					fixpoint = false;
					break;
				}
			}
			refinement_clause.clear();
			for (int i = 0; i < adf.statements.size(); i++) {
				if (new_model[i] == Interpretation::True) {
					refinement_clause.push_back(-adf.statement_true_var[adf.statements[i]]);
				} else if (new_model[i] == Interpretation::False) {
					refinement_clause.push_back(-adf.statement_false_var[adf.statements[i]]);
				} else {
					refinement_clause.push_back(adf.statement_true_var[adf.statements[i]]);
					refinement_clause.push_back(adf.statement_false_var[adf.statements[i]]);
				}
			}
			solver.add_clause(refinement_clause);
			if (fixpoint) {
				break;
			} else {
				model = new_model;
			}
		}
		interpretations.push_back(model);
	}
	return interpretations;
}

std::vector<std::vector<int>> enumerate_prf_k_bipolar(ADF & adf) {
	vector<vector<int>> interpretations;
	std::vector<int> interpretation;
	for (int i = 0; i < adf.statements.size(); i++) {
		interpretation.push_back(Interpretation::Undefined);
	}
	SAT_Solver solver = SAT_Solver();
	vector<vector<int>> kbip_clauses = k_bipolar_interpretation(adf, interpretation);
	solver.add_clauses(kbip_clauses);
	vector<vector<int>> bipolar_clauses = bipolar_interpretation(adf);
	solver.add_clauses(bipolar_clauses);
	vector<vector<int>> larger_clauses = larger_interpretation(adf, interpretation);
	solver.add_clauses(larger_clauses);
	while (true) {
		bool sat = solver.solve();
		if (!sat) {
			break;
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
		while (true) {
			vector<int> new_model = Exists::exists_adm_k_bipolar(adf, model);
			if (new_model.size() != 0) {
				model = new_model;
			} else {
				break;
			}
		}
		interpretations.push_back(model);
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
	if (interpretations.size() == 0) {
		interpretations.push_back(interpretation);
	}
	return interpretations;
}

}
