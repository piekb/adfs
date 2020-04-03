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

#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <getopt.h>

#include "ADF.h"
#include "Constants.h"
#include "Exists.h"
#include "CredAcceptance.h"
#include "SkeptAcceptance.h"
#include "Enumeration.h"
#include "Utils.h"

using namespace std;

static void show_usage() {
    cout << "USAGE: ./k++adf <sem> [options] <file>\n\n"
         << "COMMAND LINE ARGUMENTS:\n"
         << "<file>\t: Input filename for ADF instance.\n"
         << "<sem>\t: ADF semantics. <sem>={cf|nai|adm|com|prf|grd}\n\n"
         << "COMMAND LINE OPTIONS:\n"
         << "-a <arg>: Query argument for acceptance problems.\n"
         << "-c \t: Credulous acceptance. Requires the usage of -a flag.\n"
         << "-s \t: Skeptical acceptance. Requires the usage of -a flag.\n"
         << "-l \t: Output link types (att and sup).\n"
         << "-f \t: Do not use k-bipolar encodings.\n"
         << "-n \t: Do not use shortcuts for skeptical acceptance.\n"
         << "-h \t: Display this help message.\n"
         << "-v \t: Display the version of the program.\n";
}

static void show_version() {
    cout << "k++ADF (version 2018-07-06)\n"
         << "SAT-based Reasoner for Ab­stract Dia­lect­ical Frame­works\n";
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        show_version();
        show_usage();
        return 1;
    }

    string filename = argv[argc-1];
    string sem = argv[1];

    char tmp;
    string query = "";
    bool cred = false;
    bool skept = false;
    bool links = false;
    bool opt = true;
    bool kbip = true;
    int max_kbip_distance = 16;

    while ((tmp = getopt(argc, argv, "a:cslk:hvfn")) != -1) {
        switch (tmp) {
            case 'a':
                query = optarg;
                break;
            case 'c':
                cred = true;
                break;
            case 's':
                skept = true;
                break;
            case 'l':
                links = true;
                break;
            case 'k':
                max_kbip_distance = stoi(optarg);
                break;
            case 'f':
                kbip = false;
                break;
            case 'n':
                opt = false;
                break;
            case 'h':
                show_usage();
                return 0;
            case 'v':
                show_version();
                return 0;
        }
    }

    if (sem != "cf" && sem != "nai" && sem != "adm" && sem != "com" && sem != "prf" && sem != "grd") {
        cout << "Error! Semantics " << sem << " not supported.\n";
        return 1;
    }

    if (cred & skept) {
        cout << "Error! Flags for both credulous and skeptical acceptance.\n";
        return 1;
    }

    if ((cred || skept) && query == "") {
        cout << "Error! No query argument provided.\n";
        return 1;
    }

    ifstream input;
    input.open(filename);

    if (!input.good()) {
        cout << "Error! Cannot open input file.\n";
        return 1;
    }

    string line, arg, cond;
    vector<string> statements;
    vector<pair<string,string>> conditions;

    while (!input.eof()) {
        getline(input, line);
        line.erase(remove_if(line.begin(), line.end(), ::isspace), line.end());
        if (line.length() == 0 || line[0] == '/' || line[0] == '%') continue;
        if (line.length() < 5) {
            cout << "Warning! Cannot parse line: " << line << "\n";
            continue;
        }
        string op = line.substr(0,3);
        if (line.substr(0,1) == "s") {
            if (line[1] == '(' && line.find(')') != string::npos) {
                arg = line.substr(2,line.find(')')-2);
                statements.push_back(arg);
            } else if (line.substr(0,9) == "statement" && line[9] == '(' && line.find(')') != string::npos) {
                arg = line.substr(10,line.find(')')-10);
                statements.push_back(arg);
            } else {
                cout << "Warning! Cannot parse line: " << line << "\n";
            }
        } else if (line.substr(0,2) == "ac") {
            if (line[2] == '(' && line.find(',') != string::npos) {
                arg = line.substr(3,line.find(',')-3);
                cond = line.substr(line.find(',')+1,line.length()-line.find(',')-3);
                conditions.push_back(make_pair(arg,cond));
            } else {
                cout << "Warning! Cannot parse line: " << line << "\n";
            }
        } else {
            cout << "Warning! Cannot parse line: " << line << "\n";
        }
    }

    ADF adf = ADF(statements.size());
    
    for (int i = 0; i < statements.size(); i++) {
        adf.add_statement(statements[i]);
    }
    adf.initialize_statements();

    for (int i = 0; i < conditions.size(); i++) {
        adf.add_condition(conditions[i].first, conditions[i].second);
    }
    adf.initialize_conditions();


    if ((cred || skept) && find(adf.statements.begin(), adf.statements.end(), adf.statement_to_idx[query]) == adf.statements.end()) {
        cout << "Error: Invalid query argument.\n";
        return 1;
    }
    
    adf.initialize_link_types();

    if (links) {
        for (int i = 0; i < adf.sup_links.size(); i++) {
            cout << "sup(" << adf.idx_to_statement[adf.sup_links[i].first] << "," << adf.idx_to_statement[adf.sup_links[i].second] << ") ";
        }
        for (int i = 0; i < adf.att_links.size(); i++) {
            cout << "att(" << adf.idx_to_statement[adf.att_links[i].first] << "," << adf.idx_to_statement[adf.att_links[i].second] << ") ";
        }
        cout << "\n";
        return 0;
    }

    adf.opt = opt;

    int k = 0;
    for (int i = 0; i < adf.statements.size(); i++) {
        k = max(k, (int)adf.non_bipolar_parents[adf.statements[i]].size());
    }

    if (!cred & !skept) {
        vector<vector<int>> interpretations;
        if (sem == "cf") {
            interpretations = Enumeration::enumerate_cf(adf);
        } else if (sem == "nai") {
            interpretations = Enumeration::enumerate_nai(adf);
        } else if (sem == "adm") {
//		cout << k;
            if (k == 0) {
                interpretations = Enumeration::enumerate_adm_bipolar(adf);
            } else if (k < max_kbip_distance) {
                interpretations = Enumeration::enumerate_adm_k_bipolar(adf);
            } else {
                interpretations = Enumeration::enumerate_adm(adf);
            }
        } else if (sem == "com") {
            if (k == 0) {
                interpretations = Enumeration::enumerate_com_bipolar(adf);
            } else if (k < max_kbip_distance) {
                interpretations = Enumeration::enumerate_com_k_bipolar(adf);
            } else {
                interpretations = Enumeration::enumerate_com(adf);
            }
        } else if (sem == "prf") {
            if (k == 0) {
                interpretations = Enumeration::enumerate_prf_bipolar(adf);
            } else if (k < max_kbip_distance) {
                interpretations = Enumeration::enumerate_prf_k_bipolar(adf);
            } else {
                interpretations = Enumeration::enumerate_prf(adf);
            }
        } else if (sem == "grd") {
            vector<int> grounded = Exists::exists_grd(adf);
            interpretations.push_back(grounded);
        }
        for (int i = 0; i < interpretations.size(); i++) {
            print_interpretation(adf, interpretations[i]);
            cout << "\n";
        }
        return 0;
    }

    if (cred) {
        bool accepted;
        if (sem == "cf" || sem == "nai") {
            accepted = CredAcceptance::cred_cf(adf, adf.statement_to_idx[query]);
        } else if (sem == "adm" || sem == "com" || sem == "prf") {
            if (kbip) {
                if (k == 0) {
                    accepted = CredAcceptance::cred_adm_bipolar(adf, adf.statement_to_idx[query]);
                } else if (k < max_kbip_distance) { // magic number
                    accepted = CredAcceptance::cred_adm_k_bipolar(adf, adf.statement_to_idx[query]);
                } else {
                    accepted = CredAcceptance::cred_adm(adf, adf.statement_to_idx[query]);
                }
            } else {
                accepted = CredAcceptance::cred_adm(adf, adf.statement_to_idx[query]);
            }
        } else if (sem == "grd") {
            vector<int> grounded = Exists::exists_grd(adf);
            accepted = grounded[adf.statement_to_idx[query]-1] == Interpretation::True;
        }
        if (accepted) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
        return 0;
    }

    if (skept) {
        bool accepted;
        if (sem == "cf" || sem == "adm") {
            accepted = false;
        } else if (sem == "nai") {
            accepted = SkeptAcceptance::skept_nai(adf, adf.statement_to_idx[query]);
        } else if (sem == "prf") {
            if (kbip) {
                if (k == 0) {
                    accepted = SkeptAcceptance::skept_prf_bipolar(adf, adf.statement_to_idx[query]);
                } else if (k < max_kbip_distance) { // magic number
                    accepted = SkeptAcceptance::skept_prf_k_bipolar(adf, adf.statement_to_idx[query]);
                } else {
                    accepted = SkeptAcceptance::skept_prf(adf, adf.statement_to_idx[query]);
                }
            } else {
                accepted = SkeptAcceptance::skept_prf(adf, adf.statement_to_idx[query]);
            }
        } else if (sem == "grd" || sem == "com") {
            vector<int> grounded = Exists::exists_grd(adf);
            accepted = grounded[adf.statement_to_idx[query]-1] == Interpretation::True;
        }
        if (accepted) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
        return 0;
    }

    return 0;
}
