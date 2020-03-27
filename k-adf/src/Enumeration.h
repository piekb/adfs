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

#ifndef ENUMERATION_H
#define ENUMERATION_H

#include "ADF.h"

#include <vector>

namespace Enumeration {

std::vector<std::vector<int>> enumerate_cf(ADF & adf);
std::vector<std::vector<int>> enumerate_nai(ADF & adf);
std::vector<std::vector<int>> enumerate_adm(ADF & adf);
std::vector<std::vector<int>> enumerate_com(ADF & adf);
std::vector<std::vector<int>> enumerate_prf(ADF & adf);

std::vector<std::vector<int>> enumerate_adm_bipolar(ADF & adf);
std::vector<std::vector<int>> enumerate_adm_k_bipolar(ADF & adf);
std::vector<std::vector<int>> enumerate_com_bipolar(ADF & adf);
std::vector<std::vector<int>> enumerate_com_k_bipolar(ADF & adf);
std::vector<std::vector<int>> enumerate_prf_bipolar(ADF & adf);
std::vector<std::vector<int>> enumerate_prf_k_bipolar(ADF & adf);

}

#endif
