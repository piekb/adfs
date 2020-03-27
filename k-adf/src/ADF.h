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

#ifndef ADF_H
#define ADF_H

#include "Formula.h"

#include <vector>
#include <map>

class ADF {
public:
    
ADF(int n);
~ADF();

int n_statements;
int count;
int global_count;
bool opt;

/*!
 * Statements and acceptance conditions of the ADF instance.
 */
std::vector<int> statements;
std::vector<std::vector<std::vector<int>>> statement_clauses;
std::vector<std::vector<std::vector<int>>> statement_clauses_;


std::vector<Formula> conditions;
std::vector<std::vector<std::vector<int>>> condition_clauses;

std::map<int,std::vector<int>> parents;
std::map<int,std::vector<int>> range;
std::map<int,std::vector<int>> sup_parents;
std::map<int,std::vector<int>> sup_range;
std::map<int,std::vector<int>> att_parents;
std::map<int,std::vector<int>> att_range;
std::map<int,std::vector<int>> redundant_parents;
std::map<int,std::vector<int>> redundant_range;
std::map<int,std::vector<int>> non_bipolar_parents;
std::map<int,std::vector<int>> non_bipolar_range;

std::vector<std::pair<int,int>> links;
std::vector<std::pair<int,int>> sup_links;
std::vector<std::pair<int,int>> att_links;
std::vector<std::pair<int,int>> redundant_links;
std::vector<std::pair<int,int>> non_bipolar_links;

std::map<std::string,int> statement_to_idx;
std::map<int,std::string> idx_to_statement;

int true_var;
int false_var;

std::map<int,int> statement_true_var;
std::map<int,int> statement_false_var;

std::map<int,int> statement_var;
std::map<std::pair<int,int>,int> condition_var;
std::map<int,std::pair<int,int>> condition_var_to_pair;

void add_statement(std::string statement);
void add_condition(std::string statement, std::string condition);
void initialize_statements();
void initialize_conditions();
void initialize_link_types();

};

#endif
