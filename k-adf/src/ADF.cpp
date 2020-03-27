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

#include "ADF.h"
#include "Polarity.h"
#include "Utils.h"

ADF::ADF(int n) {
    n_statements = 0;
    count = 0;
    global_count = 2;
    true_var = 1;
    false_var = 2;
    opt = true;
    conditions.reserve(n);
}

ADF::~ADF() {
    for (int i = 0; i < conditions.size(); i++) {
        conditions[i].destroy_tree(conditions[i].root);
    }
}

void ADF::add_statement(std::string statement) {
    statements.push_back(++n_statements);
    statement_to_idx[statement] = n_statements;
    idx_to_statement[n_statements] = statement;
}

void ADF::add_condition(std::string statement, std::string condition) {
    Formula formula = Formula(count);
    formula.true_var = 1;
    formula.false_var = 2;
    formula.global_count = global_count;
    for (int i = 0; i < statements.size(); i++) {
        formula.global_var_to_idx[idx_to_statement[statements[i]]] = statement_var[statements[i]];
    }
    formula.parse(condition);
    count = formula.count;
    global_count = formula.global_count;
    conditions[statement_to_idx[statement]-1] = formula;
}

void ADF::initialize_statements() {
    true_var = ++count;
    false_var = ++count;
    for (int i = 0; i < statements.size(); i++) {
        statement_true_var[statements[i]] = ++count;
        statement_false_var[statements[i]] = ++count;
        statement_var[statements[i]] = ++global_count;        
    }
}

void ADF::initialize_conditions() {
    for (int i = 0; i < statements.size(); i++) {
        condition_clauses.push_back(conditions[i].to_cnf(false));
        statement_clauses.push_back(conditions[i].to_cnf(true));
        for (auto parent : conditions[i].vars_set) {
            condition_var[std::make_pair(statement_to_idx[parent],statements[i])] = conditions[i].var_to_idx[parent];
            condition_var_to_pair[conditions[i].var_to_idx[parent]] = std::make_pair(statement_to_idx[parent],statements[i]);
            parents[statements[i]].push_back(statement_to_idx[parent]);
            range[statement_to_idx[parent]].push_back(statements[i]);
            links.push_back(std::make_pair(statement_to_idx[parent], statements[i]));
        }
    }
}

void ADF::initialize_link_types() {
    for (int i = 0; i < links.size(); i++) {
        bool sup = false;
        bool att = false;
        if (Polarity::link_is_sup(*this, links[i])) {
            sup = true;
        }
        if (Polarity::link_is_att(*this, links[i])) {
            att = true;
        }
        if (!sup && !att) {
            non_bipolar_links.push_back(links[i]);
            non_bipolar_parents[links[i].second].push_back(links[i].first);
            non_bipolar_range[links[i].first].push_back(links[i].second);
        } else if (sup & !att) {
            sup_links.push_back(links[i]);
            sup_parents[links[i].second].push_back(links[i].first);
            sup_range[links[i].first].push_back(links[i].second);
        } else if (att & !sup) {
            att_links.push_back(links[i]);
            att_parents[links[i].second].push_back(links[i].first);
            att_range[links[i].first].push_back(links[i].second);
        } else {
            redundant_links.push_back(links[i]);
            redundant_parents[links[i].second].push_back(links[i].first);
            redundant_range[links[i].first].push_back(links[i].second);
        }
    }
}
