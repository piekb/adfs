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

#ifndef FORMULA_H
#define FORMULA_H

#include "Node.h"

#include <vector>
#include <map>
#include <set>

class Formula {

public:
	Formula(int c);
    ~Formula();
	void parse(std::string input);
	void print();
	std::vector<std::vector<int>> node_to_cnf(node * node, bool global);
	std::vector<std::vector<int>> to_cnf(bool global);
	void destroy_tree(node * leaf);
	void print_node(node * node);
	node * root;
    node * parse_node(std::string & input);
    std::vector<int> vars;
    std::set<std::string> vars_set;
    std::map<std::string,int> var_to_idx;
    std::map<int,std::string> idx_to_var;
    std::map<std::string,int> global_var_to_idx;
    int count;
    int global_count;
    int true_var;
    int false_var;
};

#endif
