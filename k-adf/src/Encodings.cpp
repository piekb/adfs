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

#include "Encodings.h"
#include "Constants.h"
#include "Utils.h"
#include <iostream>

using namespace std;

vector<vector<int>> cf_interpretation(ADF & adf) {
	vector<vector<int>> clauses;
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	clauses.push_back(true_clause);
	clauses.push_back(false_clause);
	for (int i = 0; i < adf.condition_clauses.size(); i++) {
		clauses.insert(clauses.end(), adf.condition_clauses[i].begin(), adf.condition_clauses[i].end());
	}
	//print_clauses(clauses);
	for (int i = 0; i < adf.statements.size(); i++) {
		vector<int> clause;
		//std::cout << -adf.statement_true_var[adf.statements[i]] << " ";
		clause.push_back(-adf.statement_true_var[adf.statements[i]]);
		int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->value;
		clause.push_back(val);
		//std::cout << val << " ";
		clauses.push_back(clause);
		clause.clear();
		for (int j = 0; j < adf.range[adf.statements[i]].size(); j++) {
			clause.push_back(-adf.statement_true_var[adf.statements[i]]);
			clause.push_back(adf.condition_var[make_pair(adf.statements[i], adf.range[adf.statements[i]][j])]);
			clauses.push_back(clause);
			clause.clear();
		}
	}
	for (int i = 0; i < adf.statements.size(); i++) {
		vector<int> clause;
		//std::cout << -adf.statement_false_var[adf.statements[i]] << " ";
		clause.push_back(-adf.statement_false_var[adf.statements[i]]);
		int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->value;
		clause.push_back(-val);
		//std::cout << -val << " ";
		clauses.push_back(clause);
		clause.clear();
		for (int j = 0; j < adf.range[adf.statements[i]].size(); j++) {
			clause.push_back(-adf.statement_false_var[adf.statements[i]]);
			clause.push_back(-adf.condition_var[make_pair(adf.statements[i], adf.range[adf.statements[i]][j])]);
			clauses.push_back(clause);
			clause.clear();
		}
	}
	return clauses;
}

vector<vector<int>> larger_interpretation(ADF & adf, std::vector<int> & interpretation) {
	vector<vector<int>> clauses;
	for (int i = 0; i < adf.statements.size(); i++) {
		vector<int> clause;
		clause.push_back(-adf.statement_true_var[adf.statements[i]]);
		clause.push_back(-adf.statement_false_var[adf.statements[i]]);
		clauses.push_back(clause);
	}
	vector<int> undef_clause;
	for (int i = 0; i < interpretation.size(); i++) {
		if (interpretation[i] == Interpretation::True) {
			vector<int> clause;
			clause.push_back(adf.statement_true_var[adf.statements[i]]);
			clauses.push_back(clause);
		} else if (interpretation[i] == Interpretation::False) {
			vector<int> clause;
			clause.push_back(adf.statement_false_var[adf.statements[i]]);
			clauses.push_back(clause);
		} else {
			undef_clause.push_back(adf.statement_true_var[adf.statements[i]]);
			undef_clause.push_back(adf.statement_false_var[adf.statements[i]]);
		}
	}
	clauses.push_back(undef_clause);
	//print_clauses(clauses);
	return clauses;
}

vector<vector<int>> adm_verification(ADF & adf, vector<int> & interpretation) {
	vector<vector<int>> clauses;
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	clauses.push_back(true_clause);
	clauses.push_back(false_clause);
	for (int i = 0; i < adf.statement_clauses.size(); i++) {
		clauses.insert(clauses.end(), adf.statement_clauses[i].begin(), adf.statement_clauses[i].end());
	}
	//cout << i << " ";
//	print_clauses(clauses);
//	std::cout << "------";
	for (int i = 0; i < interpretation.size(); i++) {
		if (interpretation[i] == Interpretation::True) {
			vector<int> clause;
			clause.push_back(adf.statement_var[adf.statements[i]]);
			clauses.push_back(clause);
		} else if (interpretation[i] == Interpretation::False) {
			vector<int> clause;
			clause.push_back(-adf.statement_var[adf.statements[i]]);
			clauses.push_back(clause);
		}
	}
	vector<int> not_adm_clause;
	for (int i = 0; i < interpretation.size(); i++) {
		int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->global_value;
		if (interpretation[i] == Interpretation::True) {
			not_adm_clause.push_back(-val);
		} else if (interpretation[i] == Interpretation::False) {
			not_adm_clause.push_back(val);
		}
	}
	clauses.push_back(not_adm_clause);
	return clauses;	
}

vector<vector<int>> bipolar_interpretation(ADF & adf) {
	vector<vector<int>> clauses;
	for (int i = 0; i < adf.statements.size(); i++) {
		for (int j = 0; j < adf.att_parents[adf.statements[i]].size(); j++) {
			vector<int> clause;
			clause.push_back(-adf.statement_true_var[adf.statements[i]]);
			clause.push_back(adf.statement_false_var[adf.att_parents[adf.statements[i]][j]]);
			clause.push_back(adf.condition_var[make_pair(adf.att_parents[adf.statements[i]][j], adf.statements[i])]);;
			clauses.push_back(clause);
		}
		for (int j = 0; j < adf.sup_parents[adf.statements[i]].size(); j++) {
			vector<int> clause;
			clause.push_back(-adf.statement_true_var[adf.statements[i]]);
			clause.push_back(adf.statement_true_var[adf.sup_parents[adf.statements[i]][j]]);
			clause.push_back(-adf.condition_var[make_pair(adf.sup_parents[adf.statements[i]][j], adf.statements[i])]);;
			clauses.push_back(clause);
		}
		for (int j = 0; j < adf.att_parents[adf.statements[i]].size(); j++) {
			vector<int> clause;
			clause.push_back(-adf.statement_false_var[adf.statements[i]]);
			clause.push_back(adf.statement_true_var[adf.att_parents[adf.statements[i]][j]]);
			clause.push_back(-adf.condition_var[make_pair(adf.att_parents[adf.statements[i]][j], adf.statements[i])]);;
			clauses.push_back(clause);
		}
		for (int j = 0; j < adf.sup_parents[adf.statements[i]].size(); j++) {
			vector<int> clause;
			clause.push_back(-adf.statement_false_var[adf.statements[i]]);
			clause.push_back(adf.statement_false_var[adf.sup_parents[adf.statements[i]][j]]);
			clause.push_back(adf.condition_var[make_pair(adf.sup_parents[adf.statements[i]][j], adf.statements[i])]);;
			clauses.push_back(clause);
		}
	}
	return clauses;
}

vector<vector<int>> k_bipolar_interpretation(ADF & adf, vector<int> & interpretation) {
	vector<vector<int>> clauses;
	vector<int> true_clause = {adf.true_var};
	vector<int> false_clause = {-adf.false_var};
	clauses.push_back(true_clause);
	clauses.push_back(false_clause);
	
	map<int,vector<int>> statement_to_non_bip_parents;
	map<int,vector<int>> statement_to_root_values;
	map<int,int> root_value_to_interpretation;

	int count = 0;
	for (int i = 0; i < adf.statements.size(); i++) {
		vector<int> root_values;
		vector<int> non_bip_parents;
		map<int,bool> is_non_bip_parent;
		map<int,int> non_bip_parent_to_idx;
		for (int j = 0; j < adf.non_bipolar_parents[adf.statements[i]].size(); j++) {
			if (interpretation[adf.non_bipolar_parents[adf.statements[i]][j]-1] == Interpretation::Undefined) {
				non_bip_parent_to_idx[adf.non_bipolar_parents[adf.statements[i]][j]] = non_bip_parents.size();
				non_bip_parents.push_back(adf.non_bipolar_parents[adf.statements[i]][j]);
				is_non_bip_parent[adf.non_bipolar_parents[adf.statements[i]][j]] = true;
			}
		}
		statement_to_non_bip_parents[adf.statements[i]] = non_bip_parents;
		int k = non_bip_parents.size();
		if (k == 0) {
			clauses.insert(clauses.end(), adf.condition_clauses[i].begin(), adf.condition_clauses[i].end());
			continue;
		}
		for (int j = 0; j < (1<<k); j++) {
			int root_value = 0;
			vector<vector<int>> new_condition_clauses;
			map<int,int> var_to_new_var;
			for (int l = 0; l < adf.condition_clauses[i].size(); l++) {
				vector<int> clause;
				for (int m = 0; m < adf.condition_clauses[i][l].size(); m++) {
					int current_var = abs(adf.condition_clauses[i][l][m]);
					if (adf.condition_var_to_pair.find(current_var) == adf.condition_var_to_pair.end()) {
						if (var_to_new_var.find(current_var) == var_to_new_var.end()) {
							var_to_new_var[current_var] = adf.count + ++count;
							if (current_var == adf.conditions[i].root->value) {
								root_value = var_to_new_var[current_var];
							}
						}
						clause.push_back((adf.condition_clauses[i][l][m] > 0) ? var_to_new_var[current_var] : -var_to_new_var[current_var]);
					} else {
						pair<int,int> link = adf.condition_var_to_pair[current_var];
						if (is_non_bip_parent[link.first]) {
							if (j & (1<<non_bip_parent_to_idx[link.first])) {
								clause.push_back((adf.condition_clauses[i][l][m] > 0) ? adf.true_var : -adf.true_var);
							} else {
								clause.push_back((adf.condition_clauses[i][l][m] > 0) ? adf.false_var : -adf.false_var);
							}
						} else {
							clause.push_back((adf.condition_clauses[i][l][m] > 0) ? current_var : -current_var);
						}
					}
				}
				new_condition_clauses.push_back(clause);
			}
			clauses.insert(clauses.end(), new_condition_clauses.begin(), new_condition_clauses.end());
			if (root_value) {
				root_values.push_back(root_value);
				root_value_to_interpretation[root_value] = j;
			}
		}
		statement_to_root_values[adf.statements[i]] = root_values;
	}
	for (int i = 0; i < adf.statements.size(); i++) {
		if (statement_to_root_values[adf.statements[i]].size() != 0) {
			for (int j = 0; j < statement_to_root_values[adf.statements[i]].size(); j++) {
				int val = (adf.conditions[i].root-> neg ? -1 : 1) * statement_to_root_values[adf.statements[i]][j];
				int interp = root_value_to_interpretation[statement_to_root_values[adf.statements[i]][j]];
				vector<int> clause;
				clause.push_back(-adf.statement_true_var[adf.statements[i]]);
				for (int k = 0; k < statement_to_non_bip_parents[adf.statements[i]].size(); k++) {
					if (interp & (1 << k)) {
						clause.push_back(adf.statement_false_var[statement_to_non_bip_parents[adf.statements[i]][k]]);
					} else {
						clause.push_back(adf.statement_true_var[statement_to_non_bip_parents[adf.statements[i]][k]]);
					}
				}
				clause.push_back(val);
				clauses.push_back(clause);
			}
		} else {
			vector<int> clause;
			clause.push_back(-adf.statement_true_var[adf.statements[i]]);
			int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->value;
			clause.push_back(val);
			clauses.push_back(clause);
		}
		for (int j = 0; j < adf.range[adf.statements[i]].size(); j++) {
			vector<int> clause;
			clause.push_back(-adf.statement_true_var[adf.statements[i]]);
			clause.push_back(adf.condition_var[make_pair(adf.statements[i], adf.range[adf.statements[i]][j])]);
			clauses.push_back(clause);
		}
		if (statement_to_root_values[adf.statements[i]].size() != 0) {
			for (int j = 0; j < statement_to_root_values[adf.statements[i]].size(); j++) {
				int val = (adf.conditions[i].root-> neg ? -1 : 1) * statement_to_root_values[adf.statements[i]][j];
				int interp = root_value_to_interpretation[statement_to_root_values[adf.statements[i]][j]];
				vector<int> clause;
				clause.push_back(-adf.statement_false_var[adf.statements[i]]);
				for (int k = 0; k < statement_to_non_bip_parents[adf.statements[i]].size(); k++) {
					if (interp & (1 << k)) {
						clause.push_back(adf.statement_false_var[statement_to_non_bip_parents[adf.statements[i]][k]]);
					} else {
						clause.push_back(adf.statement_true_var[statement_to_non_bip_parents[adf.statements[i]][k]]);
					}
				}
				clause.push_back(-val);
				clauses.push_back(clause);
			}
		} else {
			vector<int> clause;
			clause.push_back(-adf.statement_false_var[adf.statements[i]]);
			int val = (adf.conditions[i].root->neg ? -1 : 1) * adf.conditions[i].root->value;
			clause.push_back(-val);
			clauses.push_back(clause);
		}
		for (int j = 0; j < adf.range[adf.statements[i]].size(); j++) {
			vector<int> clause;
			clause.push_back(-adf.statement_false_var[adf.statements[i]]);
			clause.push_back(-adf.condition_var[make_pair(adf.statements[i], adf.range[adf.statements[i]][j])]);
			clauses.push_back(clause);
			clause.clear();
		}
	}
	return clauses;
}
