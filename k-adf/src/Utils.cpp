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

#include "Constants.h"
#include "Utils.h"

#include <iostream>

void print_clause(std::vector<int> & v) {
	for (int i = 0; i < v.size(); i++) {
		std::cout << v[i] << " ";
	}
	std::cout << "0\n";
}

void print_clauses(std::vector<std::vector<int>> & v) {
	for (int i = 0; i < v.size(); i++) {
		print_clause(v[i]);
	}
}

void print_interpretation(ADF & adf, std::vector<int> & v) {
	for (int i = 0; i < v.size(); i++) {
		if (v[i] == Interpretation::True) {
        	std::cout << "t(" << adf.idx_to_statement[adf.statements[i]] << ") ";
        }
        /*else if (v[i] == Interpretation::False) {
        	std::cout << "f(" << adf.idx_to_statement[adf.statements[i]] << ") ";
        } else {
        	std::cout << "u(" << adf.idx_to_statement[adf.statements[i]] << ") ";
        }*/
	}
	for (int i = 0; i < v.size(); i++) {
		if (v[i] == Interpretation::False) {
        	std::cout << "f(" << adf.idx_to_statement[adf.statements[i]] << ") ";
        }
    }
    for (int i = 0; i < v.size(); i++) {
		if (v[i] == Interpretation::Undefined) {
        	std::cout << "u(" << adf.idx_to_statement[adf.statements[i]] << ") ";
        }
    }
	std::cout << "\n";
}
