#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################################
# Copyright 2015 Dominik Rueß - dominik.ruess@gmx.de                     #
#                                                                        #
# this file is part of "pure python polyfit"                             #
#                                                                        #
# "pure python polyfit" is free software: you can redistribute           #
# it and/or modify it under the terms of the GNU General Public License  #
# as published by the Free Software Foundation, either version 3 of the  #
# License, or (at your option) any later version.                        #
#                                                                        #
# "pure python polyfit" is distributed in the hope that it will          #
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty #
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU    #
# General Public License for more details.                               #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with "pure python polyfit".                                      #
# If not, see http://www.gnu.org/licenses/.                              #
##########################################################################

"""
For testing, I compare the results to numpy outputs
"""

# sys imports
import functools
import unittest

import numpy as np
import operator
import sys
from itertools import product

from purePythonPolyFit import PolyFit, PolyFit2D, PolyFitND
from purePythonPolyFit import elementWise, transpose
from purePythonPolyFit import eyeMatrix, matrixMultiplication, norm
from purePythonPolyFit import leastSquareSolution, qr


class testGeometry(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)

    def testMatrixMultiplication(self):
        for i in range(50):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i, i * 2)
            A2 = np.random.rand(i, i * 2)
            B1 = np.random.rand(i * 2, i * 3)
            B2 = np.random.rand(i * 2, i * 3)

            A = A1 - A2
            B = B1 - B2

            res1 = matrixMultiplication(A.tolist(), B.tolist())
            res2 = np.dot(A, B)
            d = np.linalg.norm(res1 - res2)
            self.assertAlmostEqual(d, 0)

    def testEyeMatrix(self):
        for i in range(50):
            A = np.eye(i)
            B = eyeMatrix(i)

            d = np.linalg.norm(A - np.array(B))
            self.assertAlmostEqual(d, 0)

    def testNorm(self):
        for i in range(50):
            A1 = np.random.rand(i, i * 2)
            A2 = np.random.rand(i, i * 2)
            A = A1 - A2

            d = np.linalg.norm(A) - norm(A.tolist())
            self.assertAlmostEqual(d, 0)

        for i in range(250):
            A1 = np.random.rand(i)
            A2 = np.random.rand(i)
            A = A1 - A2

            d = np.linalg.norm(A) - norm(A.tolist())
            self.assertAlmostEqual(d, 0)

    def testElementWise(self):
        for i in range(50):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3, i * 2)
            A2 = np.random.rand(i * 3, i * 2)
            B1 = np.random.rand(i * 3, i * 2)
            B2 = np.random.rand(i * 3, i * 2)

            A = A1 - A2
            B = B1 - B2

            res1 = elementWise(A.tolist(), B.tolist(), lambda x, y: x - y)
            res2 = A - B
            d = np.linalg.norm(res1 - res2)
            self.assertAlmostEqual(d, 0)

            res1 = elementWise(A.tolist(), B.tolist(), lambda x, y: x + y)
            res2 = A + B
            d = np.linalg.norm(res1 - res2)
            self.assertAlmostEqual(d, 0)

            res1 = elementWise(A.tolist(), B.tolist(), lambda x, y: x * y)
            res2 = A * B
            d = np.linalg.norm(res1 - res2)
            self.assertAlmostEqual(d, 0)

            res1 = elementWise(A.tolist(), B.tolist(), lambda x, y: x / y)
            res2 = A / B
            d = np.linalg.norm(res1 - res2)
            self.assertAlmostEqual(d, 0)

    def testQr(self):
        for i in range(11):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3, i * 4)
            A2 = np.random.rand(i * 3, i * 4)
            A = A1 - A2

            Q1, R1 = qr(A)
            d = np.linalg.norm(A - np.dot(Q1, R1))
            self.assertAlmostEqual(d, 0)
            # check upper triangle
            for j in range(i):
                for k in range(j):
                    self.assertAlmostEqual(R1[j][k], 0)

        # over determined (unique solution up to signs of R diagonal elements)

        for i in range(1, 11):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3, i * 2)
            A2 = np.random.rand(i * 3, i * 2)
            A = A1 - A2

            Q1, R1 = qr(A)
            Q2, R2 = np.linalg.qr(A)
            d = np.linalg.norm(A - np.dot(Q1, R1))
            self.assertAlmostEqual(d, 0)
            self.assertAlmostEqual(np.linalg.norm(Q2 - Q1), 0)
            self.assertAlmostEqual(np.linalg.norm(R2 - R1), 0)
            # check upper triangle
            for j in range(i):
                for k in range(j):
                    self.assertAlmostEqual(R1[j][k], 0)

    def testTranspose(self):
        for i in range(110):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3, i * 4)
            A2 = np.random.rand(i * 3, i * 4)
            A = A1 - A2

            At = transpose(A.tolist())
            Att = transpose(At)

            d = np.linalg.norm(A - Att)
            self.assertAlmostEqual(d, 0)

            d = np.linalg.norm(A.transpose() - At)
            self.assertAlmostEqual(d, 0)

    def testLeastSquareSolution(self):
        # over determined:
        for i in range(1, 11):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3, i * 2)
            A2 = np.random.rand(i * 3, i * 2)
            B1 = np.random.rand(i * 3)
            B2 = np.random.rand(i * 3)

            A = A1 - A2
            b = B1 - B2

            s2, r2, rk, _ = np.linalg.lstsq(A, b)
            s1, r1 = leastSquareSolution(A.tolist(), b.tolist())
            d = np.linalg.norm(s2 - s1)
            self.assertAlmostEqual(d, 0)

        # under determined:
        for i in range(1, 11):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3, i * 4)
            A2 = np.random.rand(i * 3, i * 4)
            B1 = np.random.rand(i * 3)
            B2 = np.random.rand(i * 3)

            A = A1 - A2
            b = B1 - B2

            s2, r2, _, _ = np.linalg.lstsq(A, b)
            s1, r1 = leastSquareSolution(A.tolist(), b.tolist())
            d = np.linalg.norm(r2 - r1)
            self.assertAlmostEqual(d, 0)

    def testPolyFit(self):
        testCoords = np.arange(-1, 1, 0.1)
        for i in range(1, 5):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3)
            A2 = np.random.rand(i * 3)

            A = A1 - A2
            for j in range(1, 5):
                B1 = np.random.rand(j)
                B2 = np.random.rand(j)
                B = (B1 - B2) / 100.0
                pTs = np.polynomial.polynomial.polyval(A, B)
                # + np.random.randn(i*3)/100.0
                p1 = PolyFit(A, pTs, order=j)
                # p2 = np.polynomial.polynomial.polyfit(A, pTs, j)
                # for x in testCoords:
                #     v2 = np.polynomial.polynomial.polyval(x, p2)
                #     self.assertAlmostEqual(p1[x], v2)
                for i, x in enumerate(A.tolist()):
                    self.assertAlmostEqual(p1[x], pTs[i])

    def testPolyFit2D(self):
        testCoords = np.arange(-1, 1, 0.1)
        for i in range(1, 15):
            sys.stdout.write('.')
            sys.stdout.flush()
            A1 = np.random.rand(i * 3, 2)
            A2 = np.random.rand(i * 3, 2)
            A = A1 - A2

            for j in range(1, 5):
                m = [x for x in product(range(j + 1), range(j + 1)) if x[0] + x[1] <= j]
                l = len(m)
                u1 = np.random.rand(l)
                u2 = np.random.rand(l)
                u = (u1 - u2) / 100.0

                pTs = [sum([u.tolist()[o] * A[k, 0] ** m[o][0] * A[k, 1] ** m[o][1]
                            for o in range(l)])
                       for k in range(A.shape[0])]

                p1 = PolyFit2D(A.tolist(), pTs, order=j)
                for i, x in enumerate(A.tolist()):
                    self.assertAlmostEqual(p1[x], pTs[i])

    def testPolyFitND(self):
        testCoords = np.arange(-1, 1, 0.1)
        for d in range(1, 5):
            for i in range(1, 15):
                samplings = (np.random.rand(i * 3, d) - np.random.rand(i * 3, d)).tolist()

                for j in range(1, 5):
                    sys.stdout.write('.')
                    sys.stdout.flush()

                    m = [x for x in product(*[range(j + 1)] * d) if sum(x) <= j]
                    l = len(m)
                    u1 = np.random.rand(l)
                    u2 = np.random.rand(l)
                    u = ((u1 - u2) / 100.0).tolist()

                    pTs = [sum([u[o] * functools.reduce(operator.mul, [samplings[v][k] ** m[o][k] for k in range(d)], 1)
                                for o in range(l)]) for v in range(len(samplings))]

                    p1 = PolyFitND(samplings, pTs, order=j)
                    for i, x in enumerate(samplings):
                        self.assertAlmostEqual(p1[x], pTs[i])


if __name__ == '__main__':
    unittest.main()
