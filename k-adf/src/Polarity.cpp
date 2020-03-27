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

#include "Polarity.h"

#if defined(SAT_MINISAT)
#include "MiniSATSolver.h"
typedef MiniSATSolver SAT_Solver;
#else
#error "No SAT solver defined"
#endif

using namespace std;

namespace Polarity {

bool link_is_sup(ADF & adf, std::pair<int,int> link) {
	int b = link.first;
	int a = link.second;
	SAT_Solver solver = SAT_Solver();
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	solver.add_clause(true_clause);
	solver.add_clause(false_clause);
	vector<vector<int>> statement_clauses = adf.statement_clauses[a-1];
	solver.add_clauses(statement_clauses);
	int adf_vars = adf.statements.size() + 2;
	if (statement_clauses.size() != 0) {
		int count = 0;
		int root_value_flipped = 0;
		vector<vector<int>> statement_clauses_flipped;
		map<int,int> var_to_flipped_var;
		for (int i = 0; i < statement_clauses.size(); i++) {
			vector<int> clause;
			for (int j = 0; j < statement_clauses[i].size(); j++) {
				int current_var = abs(statement_clauses[i][j]);
				if (current_var > adf_vars) {
					if (var_to_flipped_var.find(current_var) == var_to_flipped_var.end()) {
						var_to_flipped_var[current_var] = solver.n_vars + ++count;
						if (current_var == adf.conditions[a-1].root->global_value) {
							root_value_flipped = var_to_flipped_var[current_var];
						}
					}
					clause.push_back((statement_clauses[i][j] > 0) ? var_to_flipped_var[current_var] : - var_to_flipped_var[current_var]);
				} else {
					if (current_var == adf.statement_var[b]) {
						current_var = -current_var;
					}
					clause.push_back((statement_clauses[i][j] > 0) ? current_var : -current_var);
				}
			}
			statement_clauses_flipped.push_back(clause);
		}
		solver.add_clauses(statement_clauses_flipped);
		vector<int> clause1;
		clause1.push_back(-adf.statement_var[b]);
		solver.add_clause(clause1);
		vector<int> clause2;
		clause2.push_back((adf.conditions[a-1].root->neg ? -1 : 1)*adf.conditions[a-1].root->global_value);
		solver.add_clause(clause2);
		vector<int> clause3;
		clause3.push_back(-(adf.conditions[a-1].root->neg ? -1 : 1)*root_value_flipped);
		solver.add_clause(clause3);
	} else {
		vector<int> clause1;
		clause1.push_back(-adf.statement_var[b]);
		solver.add_clause(clause1);
		vector<int> clause2;
		clause2.push_back((adf.conditions[a-1].root->neg ? -1 : 1)*adf.conditions[a-1].root->global_value);
		solver.add_clause(clause2);
	}
	bool sat = solver.solve();
	return !sat;
}

bool link_is_att(ADF & adf, std::pair<int,int> link) {
	int b = link.first;
	int a = link.second;
	SAT_Solver solver = SAT_Solver();
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	solver.add_clause(true_clause);
	solver.add_clause(false_clause);
	vector<vector<int>> statement_clauses = adf.statement_clauses[a-1];
	solver.add_clauses(statement_clauses);
	int adf_vars = adf.statements.size() + 2;
	if (statement_clauses.size() != 0) {
		int count = 0;
		int root_value_flipped = 0;
		vector<vector<int>> statement_clauses_flipped;
		map<int,int> var_to_flipped_var;
		for (int i = 0; i < statement_clauses.size(); i++) {
			vector<int> clause;
			for (int j = 0; j < statement_clauses[i].size(); j++) {
				int current_var = abs(statement_clauses[i][j]);
				if (current_var > adf_vars) {
					if (var_to_flipped_var.find(current_var) == var_to_flipped_var.end()) {
						var_to_flipped_var[current_var] = solver.n_vars + ++count;
						if (current_var == adf.conditions[a-1].root->global_value) {
							root_value_flipped = var_to_flipped_var[current_var];
						}
					}
					clause.push_back((statement_clauses[i][j] > 0) ? var_to_flipped_var[current_var] : - var_to_flipped_var[current_var]);
				} else {
					if (current_var == adf.statement_var[b]) {
						current_var = -current_var;
					}
					clause.push_back((statement_clauses[i][j] > 0) ? current_var : -current_var);
				}
			}
			statement_clauses_flipped.push_back(clause);
		}
		solver.add_clauses(statement_clauses_flipped);
		vector<int> clause1;
		clause1.push_back(-adf.statement_var[b]);
		solver.add_clause(clause1);
		vector<int> clause2;
		clause2.push_back(-(adf.conditions[a-1].root->neg ? -1 : 1)*adf.conditions[a-1].root->global_value);
		solver.add_clause(clause2);
		vector<int> clause3;
		clause3.push_back((adf.conditions[a-1].root->neg ? -1 : 1)*root_value_flipped);
		solver.add_clause(clause3);
	} else {
		vector<int> clause1;
		clause1.push_back(-adf.statement_var[b]);
		solver.add_clause(clause1);
		vector<int> clause2;
		clause2.push_back(-(adf.conditions[a-1].root->neg ? -1 : 1)*adf.conditions[a-1].root->global_value);
		solver.add_clause(clause2);
	}
	bool sat = solver.solve();
	return !sat;
}

}
