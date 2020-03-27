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

#include "Formula.h"
#include "Constants.h"

#include <iostream>

Formula::Formula(int c) {
	root = NULL;
	count = c;
	true_var = c;
	false_var = c;
}

Formula::~Formula() {
	//destroy_tree(root);
}

void Formula::destroy_tree(node * leaf) {
	if(leaf != NULL) {
    	destroy_tree(leaf->left);
    	destroy_tree(leaf->right);
    	delete leaf;
  	}
}

node * Formula::parse_node(std::string & input) {
	bool is_var = false;
	bool neg = false;
	int value = -1;
	int global_value = -1;
	int oper = -1;
	std::string tmp = input;
	while (tmp.substr(0,4) == "neg(") {
		neg = !neg;
		tmp = tmp.substr(4);
		tmp = tmp.substr(0,tmp.length()-1);
	}
	if (tmp.substr(0,4) == "and(") {
		value = ++count;
		global_value = ++global_count;
		oper = Logic::And;
		tmp = tmp.substr(4);
		tmp = tmp.substr(0, tmp.length()-1);
		node * node = new_node(is_var, neg, value, global_value, oper);
		int count_left = 0;
		int count_right = 0;
		int position = 0;
		for (int i = 0; i < tmp.length(); i++) {
			if (tmp[i] == '(') {
				count_left++;
			} else if (tmp[i] == ')') {
				count_right++;
			} else if (tmp[i] == ',') {
				if (count_left == count_right) {
					position = i;
					break;
				}
			}
		}
		std::string tmp_left = tmp.substr(0,position);
		std::string tmp_right = tmp.substr(position+1,tmp.length());
		node->left = parse_node(tmp_left);
		node->right = parse_node(tmp_right);
		return node;
	} else if (tmp.substr(0,3) == "or(") {
		value = ++count;
		global_value = ++global_count;
		oper = Logic::Or;
		tmp = tmp.substr(3);
		tmp = tmp.substr(0, tmp.length()-1);
		node * node = new_node(is_var, neg, value, global_value, oper);
		int count_left = 0;
		int count_right = 0;
		int position = 0;
		for (int i = 0; i < tmp.length(); i++) {
			if (tmp[i] == '(') {
				count_left++;
			} else if (tmp[i] == ')') {
				count_right++;
			} else if (tmp[i] == ',') {
				if (count_left == count_right) {
					position = i;
					break;
				}
			}
		}
		std::string tmp_left = tmp.substr(0,position);
		std::string tmp_right = tmp.substr(position+1,tmp.length());
		node->left = parse_node(tmp_left);
		node->right = parse_node(tmp_right);
		return node;
	} else if (tmp.substr(0,4) == "xor(") {
		value = ++count;
		global_value = ++global_count;
		oper = Logic::Xor;
		tmp = tmp.substr(4);
		tmp = tmp.substr(0, tmp.length()-1);
		node * node = new_node(is_var, neg, value, global_value, oper);
		int count_left = 0;
		int count_right = 0;
		int position = 0;
		for (int i = 0; i < tmp.length(); i++) {
			if (tmp[i] == '(') {
				count_left++;
			} else if (tmp[i] == ')') {
				count_right++;
			} else if (tmp[i] == ',') {
				if (count_left == count_right) {
					position = i;
					break;
				}
			}
		}
		std::string tmp_left = tmp.substr(0,position);
		std::string tmp_right = tmp.substr(position+1,tmp.length());
		node->left = parse_node(tmp_left);
		node->right = parse_node(tmp_right);
		return node;
	} else if (tmp.substr(0,4) == "imp(") {
		value = ++count;
		global_value = ++global_count;
		oper = Logic::Or;
		tmp = tmp.substr(4);
		tmp = tmp.substr(0, tmp.length()-1);
		node * node = new_node(is_var, neg, value, global_value, oper);
		int count_left = 0;
		int count_right = 0;
		int position = 0;
		for (int i = 0; i < tmp.length(); i++) {
			if (tmp[i] == '(') {
				count_left++;
			} else if (tmp[i] == ')') {
				count_right++;
			} else if (tmp[i] == ',') {
				if (count_left == count_right) {
					position = i;
					break;
				}
			}
		}
		std::string tmp_left = tmp.substr(0,position);
		std::string tmp_right = tmp.substr(position+1,tmp.length());
		node->left = parse_node(tmp_left);
		node->left->neg = !node->left->neg;
		node->right = parse_node(tmp_right);
		return node;
	} else if (tmp.substr(0,4) == "iff(") {
		value = ++count;
		global_value = ++global_count;
		oper = Logic::And;
		tmp = tmp.substr(4);
		tmp = tmp.substr(0, tmp.length()-1);
		node * node = new_node(is_var, neg, value, global_value, oper);
		int count_left = 0;
		int count_right = 0;
		int position = 0;
		for (int i = 0; i < tmp.length(); i++) {
			if (tmp[i] == '(') {
				count_left++;
			} else if (tmp[i] == ')') {
				count_right++;
			} else if (tmp[i] == ',') {
				if (count_left == count_right) {
					position = i;
					break;
				}
			}
		}
		std::string tmp_left = tmp.substr(0,position);
		std::string tmp_right = tmp.substr(position+1,tmp.length());
		std::string tmp_left_new = "imp(" + tmp_left + "," + tmp_right + ")";
		std::string tmp_right_new = "imp(" + tmp_right + "," + tmp_left + ")";
		node->left = parse_node(tmp_left_new);
		node->right = parse_node(tmp_right_new);
		return node;
	} else if (tmp.substr(0,2) == "c(") {
		is_var = true;
		tmp = tmp.substr(2,1);
		if (tmp == "v") {
			value = true_var;
			global_value = true_var;
		} else if (tmp == "f") {
			value = false_var;
			global_value = false_var;
		}
		node * node = new_node(is_var, neg, value, global_value, oper);
		return node;
	} else {
		is_var = true;
		if (vars_set.find(tmp) == vars_set.end()) {
			vars_set.insert(tmp);
			var_to_idx[tmp] = ++count;
			idx_to_var[count] = tmp;
			vars.push_back(count);
		}
		value = var_to_idx[tmp];
		global_value = global_var_to_idx[tmp];
		node * node = new_node(is_var, neg, value, global_value, oper);
		return node;
	}
}

void Formula::parse(std::string input) {
	root = parse_node(input);
}

std::vector<std::vector<int>> Formula::node_to_cnf(node * node, bool global) {
	std::vector<std::vector<int>> clauses;
	if (node->is_var) return clauses;
	std::vector<int> clause1, clause2, clause3, clause4;
	int val, val_left, val_right;
	if (!global) {
		val = node->value;
		val_left = (node->left->neg ? -1 : 1) * node->left->value;
		val_right = (node->right->neg ? -1 : 1) * node->right->value;
	} else {
		val = node->global_value;
		val_left = (node->left->neg ? -1 : 1) * node->left->global_value;
		val_right = (node->right->neg ? -1 : 1) * node->right->global_value;
	}
	if (node->oper == Logic::And) {
		clause1.push_back(val);
		clause1.push_back(-val_left);
		clause1.push_back(-val_right);
		
		clause2.push_back(-val);
		clause2.push_back(val_left);
	
		clause3.push_back(-val);
		clause3.push_back(val_right);
	} else if (node->oper == Logic::Or) {
		clause1.push_back(-val);
		clause1.push_back(val_left);
		clause1.push_back(val_right);
		
		clause2.push_back(val);
		clause2.push_back(-val_left);
	
		clause3.push_back(val);
		clause3.push_back(-val_right);
	} else if (node->oper == Logic::Xor) {
		clause1.push_back(-val);
		clause1.push_back(val_left);
		clause1.push_back(val_right);

		clause2.push_back(-val);
		clause2.push_back(-val_left);
		clause2.push_back(-val_right);

		clause3.push_back(val);
		clause3.push_back(val_left);
		clause3.push_back(-val_right);

		clause4.push_back(val);
		clause4.push_back(-val_left);
		clause4.push_back(val_right);
	}
	clauses.push_back(clause1);
	clauses.push_back(clause2);
	clauses.push_back(clause3);
	if (node->oper == Logic::Xor) {
		clauses.push_back(clause4);
	}
	std::vector<std::vector<int>> clauses_left = node_to_cnf(node->left, global);
	std::vector<std::vector<int>> clauses_right = node_to_cnf(node->right, global);
	clauses.insert(clauses.end(), clauses_left.begin(), clauses_left.end());
	clauses.insert(clauses.end(), clauses_right.begin(), clauses_right.end());
	return clauses;
}

std::vector<std::vector<int>> Formula::to_cnf(bool global) {
	std::vector<std::vector<int>> clauses = node_to_cnf(root, global);
	return clauses;
}

void Formula::print_node(node * node) {
	if (node == NULL) return;
	if (node->neg) std::cout << "N";
	if (!node->is_var) {
		if (node->oper == Logic::And) {
			std::cout << "AND";
			std::cout << node->value;
		} else if (node->oper == Logic::Or) {
			std::cout << "OR";
			std::cout << node->value;
		} else if (node->oper == Logic::Xor) {
			std::cout << "XOR";
			std::cout << node->value;
		}
		std::cout << "(";
		print_node(node->left);
		std::cout << ",";
		print_node(node->right);
		std::cout << ")";
	} else {
		if (node->value == true_var) {
			std::cout << "TRUE";
		} else if (node->value == false_var) {
			std::cout << "FALSE";
		} else {
			std::cout << idx_to_var[node->value];
		}
	}
}

void Formula::print() {
	print_node(root);
}
