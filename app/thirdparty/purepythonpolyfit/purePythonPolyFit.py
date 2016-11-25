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
Pure python polyfitting

for usage examples see end of this file

for an alternative computation of the QR decomposition with numpy, see
http://rosettacode.org/wiki/QR_decomposition#Python
"""

import copy
import functools

import operator
from itertools import product
from math import sqrt


class PolyFit:
    """
    a pure python polynomial fitting class
    initialize with x,y coordinates and values
    and evaluate with [] operator
    """
    TAG = "Polyfit 1D"

    def __init__(self, x, values, order=1):
        """
        initialize a polyfitting with x and y coordinates
        and respective functino values
        (all simple lists)
        """
        n = len(x)
        if n != len(values):
            raise PolyFitException("input values have different lengths",
                                   self.TAG)

        self.mIn, self.sIn = meanAndStandardDeviation(x)
        self.mVal, self.sVal = meanAndStandardDeviation(values)
        x = [(y - self.mIn) / self.sIn for y in x]
        values = [(y - self.mVal) / self.sVal for y in values]

        A = [[x[i] ** float(j) for j in range(order + 1)] for i in range(n)]
        self.coeffs, self.residual = leastSquareSolution(A, values)
        self.order = order

    def __getitem__(self, x):
        """
        return the estimated function value for position x
        """
        x = (x - self.mIn) / self.sIn
        val = sum([self.coeffs[i] * x ** float(i) for i in range(self.order + 1)])
        return val * self.sVal + self.mVal


class PolyFit2D:
    """
    a pure python polynomial fitting class
    initialize with a list of points (as list/tuple) and values
    and evaluate with myFit[(x,y)] operator
    """
    TAG = "Polyfit 2D"

    def __init__(self, pts, values, order=1):
        """
        initialize a polyfitting with pts = [[x1,x2], [y1,y2], ...] coordinates
        and respective function values [v1, ...]
        (all simple lists)
        """
        n = len(pts)
        for i in range(n):
            if 2 != len(pts[i]):
                raise PolyFitException("input values have different lengths",
                                       self.TAG)

        mons = [x for x in product(range(order + 1), range(order + 1))
                if x[0] + x[1] <= order]
        self.monomials = mons
        self.n = len(self.monomials)

        # scale for better approximation
        self.mInX, self.sInX = meanAndStandardDeviation([z[0] for z in pts])
        self.mInY, self.sInY = meanAndStandardDeviation([z[1] for z in pts])
        self.mVal, self.sVal = meanAndStandardDeviation(values)
        pts = [((z[0] - self.mInX) / self.sInX, (z[1] - self.mInY) / self.sInY)
               for z in pts]
        values = [(z - self.mVal) / self.sVal for z in values]

        m = self.monomials
        A = [[pts[u][0] ** m[i][0] * pts[u][1] ** m[i][1] for i in range(self.n)]
             for u in range(n)]
        self.coeffs, self.residual = leastSquareSolution(A, values)
        self.order = order

    def __getitem__(self, x):
        """
        return the estimated function value for position x
        """
        m = self.monomials
        x = ((x[0] - self.mInX) / self.sInX, (x[1] - self.mInY) / self.sInY)
        val = sum([self.coeffs[i] * x[0] ** m[i][0] * x[1] ** m[i][1]
                   for i in range(self.n)])
        return val * self.sVal + self.mVal


class PolyFitND:
    """
    a pure python polynomial fitting class
    initialize with x,y coordinates and values
    and evaluate with [] operator
    """
    TAG = "Polyfit ND"

    def __init__(self, pts, values, order=1):
        """
        initialize a polyfitting with pts = [[x1,x2 ...], [y1,y2,...], ...]
        coordinates and respective function values [v1, ...]
        (all simple lists)
        """
        n = len(pts)
        if n <= 0:
            raise PolyFitException("no input values given",
                                   self.TAG)
        dimension = len(pts[0])
        for i in range(n):
            if dimension != len(pts[i]):
                raise PolyFitException("input values have different lengths",
                                       self.TAG)

        self.dimension = dimension

        mons = [x for x in product(*[range(order + 1)] * dimension)
                if sum(x) <= order]
        self.monomials = mons
        self.n = len(self.monomials)

        m = self.monomials

        # scales
        self.scales = [(c, s) for c, s in [meanAndStandardDeviation(
            [pts[j][i] for j in range(n)])
                                           for i in range(dimension)]]
        pts = [[(pts[j][i] - self.scales[i][0]) / self.scales[i][1]
                for i in range(dimension)]
               for j in range(n)]
        self.mVal, self.sVal = meanAndStandardDeviation(values)
        values = [(z - self.mVal) / self.sVal for z in values]

        A = [[functools.reduce(operator.mul,
                               [pts[u][d] ** m[i][d] for d in range(dimension)],
                               1)
              for i in range(self.n)]
             for u in range(n)]
        self.coeffs, self.residual = leastSquareSolution(A, values)
        self.order = order

    def __getitem__(self, x):
        """
        return the estimated function value for position x
        """
        if len(x) != self.dimension:
            raise PolyFitException("input value has different length than "
                                   "initialization data",
                                   self.TAG)

        m = self.monomials
        d = len(x)
        x = [(x[i] - self.scales[i][0]) / self.scales[i][1]
             for i in range(self.dimension)]
        val = sum([self.coeffs[i]
                   * functools.reduce(operator.mul,
                                      [x[d] ** m[i][d]
                                       for d in range(self.dimension)],
                                      1)
                   for i in range(self.n)])
        return val * self.sVal + self.mVal


class PolyFitException(Exception):
    def __init__(self, message, subType):
        super(PolyFitException, self).__init__(subType + ": " + message)


EXCEPTION_MATRIX_MULTIPLICATION = "Matrix multiplication"


# class Matrix:
#     def __init__(values):
#         if 

def mean(data):
    """
    Return the arithmetic mean of data
    """
    n = len(data)
    if n < 1:
        return 0
    return sum(data) / float(n)


def meanAndStandardDeviation(data):
    """
    Return sum of square deviations of sequence data
    """
    c = mean(data)
    ss = sum((x - c) ** 2 for x in data)
    if abs(ss) < 1e-10:
        return c, 1.0
    else:
        return c, sqrt(ss / float(len(data)))


def matrixMultiplication(A, B):
    """
    return product of matrices A and B

    the input are two lists of lists where the sublists of matrix A
    have the length of matrix B
    """
    mA = len(A)
    mB = len(B)
    if mA <= 0:
        return []
    nA = len(A[0])
    if mB != nA:
        raise PolyFitException("shapes don't match %d vs %d" % (nA, mB),
                               EXCEPTION_MATRIX_MULTIPLICATION)
    if nA == 0:
        return []
    nB = len(B[0])

    for i, b in enumerate(B):
        if len(b) != nB:
            raise PolyFitException("matrix B: row %d doesn't match matrix "
                                   "shape (%d vs %d)" % (i, len(b)),
                                   EXCEPTION_MATRIX_MULTIPLICATION)

    out = [[0.0 for x in range(nB)] for y in range(mA)]
    for row in range(mA):
        for col in range(nB):
            if len(A[row]) != nA:
                raise PolyFitException("matrix A: row %d doesn't match "
                                       "matrix shape (%d vs %d)"
                                       % (row, nA, len(A[row])),
                                       EXCEPTION_MATRIX_MULTIPLICATION)
            for i in range(mB):
                out[row][col] += A[row][i] * B[i][col]
    return out


def eyeMatrix(m):
    """
    return a list of lists which represents the identity matrix of size m
    """
    out = [[0.0 for x in range(m)] for y in range(m)]
    for i in range(m):
        out[i][i] = 1.0
    return out


def norm(v):
    """
    compute the square root of the sum of all squared components of a list v
    """

    if len(v) == 0:
        return 0
    if isinstance(v[0], list):
        return sqrt(sum([y ** 2.0 for x in v for y in x]))
    else:
        return sqrt(sum([y ** 2.0 for y in v]))


def elementWise(A, B, operation):
    """
    execute an operate element wise and return result

    A and B are lists of lists (all lists of same lengths)
    operation is a function of two arguments and one return value
    """
    return [[operation(x, y)
             for x, y in zip(rowA, rowB)]
            for rowA, rowB in zip(A, B)]


def transpose(A):
    """
    return a list of lists for a Matrix A ( list of lists )
    with transposed representation of A
    """
    m = len(A)
    if m == 0:
        return []
    n = len(A[0])
    out = [[0.0 for x in range(m)] for y in range(n)]
    for r in range(m):
        for c in range(n):
            out[c][r] = A[r][c]
    return out


def qr(A, prec=1e-10):
    """
    computes a faster and economic qr decomposition similar to:
    http://www.iaa.ncku.edu.tw/~dychiang/lab/program/mohr3d/source/Jama%5CQRDecomposition.html
    """
    m = len(A)
    if m <= 0:
        return [], A
    n = len(A[0])
    Rdiag = [0] * n;
    QR = copy.deepcopy(A)
    for k in range(n):
        # Compute 2-norm of k-th column without under/overflow.
        nrm = 0.0
        for i in range(k, m):
            nrm = sqrt(nrm ** 2 + QR[i][k] ** 2)

        if abs(nrm) > prec:
            # Form k-th Householder vector.
            if k < m and QR[k][k] < 0:
                nrm = -nrm

            for i in range(k, m):
                QR[i][k] /= nrm
            if k < m:
                QR[k][k] += 1.0

            # Apply transformation to remaining columns.
            for j in range(k + 1, n):
                s = 0.0
                for i in range(k, m):
                    s += QR[i][k] * QR[i][j]
                if k < m:
                    s = -s / QR[k][k]
                for i in range(k, m):
                    QR[i][j] += s * QR[i][k]
        Rdiag[k] = -nrm;

    # compute R
    R = [[0] * n for z in range(min(m, n))]
    for i in range(m):
        for j in range(i, n):
            if i < j:
                R[i][j] = QR[i][j]
            if i == j:
                R[i][i] = Rdiag[i]

    # compute Q
    w = min(m, n)
    Q = [[0] * w for i in range(m)]
    for k in range(w - 1, -1, -1):
        if k < w:
            Q[k][k] = 1.0;
        for j in range(k, w):
            if k < m and abs(QR[k][k]) > prec:
                s = 0.0
                for i in range(k, m):
                    s += QR[i][k] * Q[i][j]
                s = -s / QR[k][k]
                for i in range(k, m):
                    Q[i][j] += s * QR[i][k]
    return Q, R


def solveWithForwardReplacement(A, b, prec=1e-10):
    """
    solve a system Ax = b with A = QR in least squares sense
    return x

    see http://de.wikipedia.org/wiki/QR-Zerlegung
    """
    if len(A) == 0:
        return []
    Q, R = qr(transpose(A))

    Rt = transpose(R)
    m = len(Rt)
    n = len(Rt[0])

    z = [0] * n
    for r in range(m):
        if abs(Rt[r][r]) < prec:
            z[r] = 1.0
            continue
        s = 0.0
        for c in range(m):
            s += z[c] * Rt[r][c]
        z[r] = (b[r] - s) / Rt[r][r]

    res = matrixMultiplication(Q, [[a] for a in z])
    res = [v for sublist in res for v in sublist]  # flatten

    return res


def solveWithBackwardReplacement(A, b, prec=1e-10):
    """
    solve a system Ax = b with A = QR in least squares sense
    return x

    see http://de.wikipedia.org/wiki/QR-Zerlegung
    """
    n = len(A)
    if n == 0:
        return []

    Q, R = qr(A)

    n = len(R[0])
    res = [0] * n

    z = matrixMultiplication(transpose(Q), [[a] for a in b])

    for r in range(n - 1, -1, -1):
        if abs(R[r][r]) < prec:
            res[r] = 1.0
            continue
        s = 0.0
        for c in range(r + 1, n):
            s += res[c] * R[r][c]
        res[r] = (z[r][0] - s) / R[r][r]

    return res


def leastSquareSolution(A, b):
    """
    return the least squares solution x for the system Ax = b

    A is a list of list while b is a list
    """
    m = len(A)
    if m == 0:
        return []
    n = len(A[0])

    if n > m:
        s = solveWithForwardReplacement(A, b)
    else:
        s = solveWithBackwardReplacement(A, b)
    remap = matrixMultiplication(A, [[a] for a in s])
    res = sum([z[0] ** 2.0 for z in elementWise(remap, [[a] for a in b],
                                                lambda x, y: x - y)])

    return s, res


if __name__ == "__main__":

    x = range(-10, 10)
    y = [0.1 + 0.01 * z ** 2.0 + z for z in x]

    p = PolyFit(x, y, order=2)

    res = [round(p[z], 2) for z in x]
    print("fitted fn results: ", res)
    diff = [round(res[i] - y[i], 2) for i in range(len(x))]
    print("residuals to orig: ", diff)

    try:
        import numpy as np

        A = np.random.randn(30, 2) * 10.0
        Q, R = np.linalg.qr(A)
        Q2, R2 = qr(A.tolist())
        print("difference to numpy (Q,R):", np.linalg.norm(Q - np.array(Q2)), np.linalg.norm(R - np.array(R2)))

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        from matplotlib.ticker import LinearLocator, FormatStrFormatter
        import matplotlib.pyplot as plt

        Xo = np.arange(-5, 5, 1.0)
        Yo = np.arange(-5, 5, 1.0)
        X, Y = np.meshgrid(Xo, Yo)
        Z = 0.1 * X - 0.5 * Y + 0.05 * X * Y + 0.1 * X ** 2.0 + 0.003 * Y ** 2.0
        Z += np.random.randn(*Z.shape)

        X2 = np.arange(-1, 9, 0.1)
        Zlin = 0.02 * X2 ** 3.0 - 0.2 * X2 ** 2.0 + 0.15 * X2 - 1.0
        Zlin += np.random.randn(*Zlin.shape) / 2.0

        # PURE PYTHON USE: convert to list of points
        cX = [z for sublist in X.tolist() for z in sublist]
        cY = [z for sublist in Y.tolist() for z in sublist]
        coords = [(x, y) for x, y in zip(cX, cY)]
        values = [z for sublist in Z.tolist() for z in sublist]
        # PURE PYTHON USE: estimate surface and evaluate
        p1d = PolyFit(X2.tolist(), Zlin.tolist(), order=3)

        p2d = PolyFit2D(coords, values, order=2)
        pnd = PolyFitND(coords, values, order=2)

        # convert back to matplotlib and numpy (evaluate) for
        # easy visualization
        Z2 = Z.copy()
        Z3 = Z.copy()
        for r in range(Z.shape[0]):
            for c in range(Z.shape[1]):
                Z2[r, c] = p2d[(X[r, c], Y[r, c])]
                Z3[r, c] = pnd[(X[r, c], Y[r, c])]

        fig = plt.figure()
        ax0 = fig.add_subplot(2, 2, 2)
        ax0.plot(X2, Zlin, 'r^', ms=14)
        ax0.plot(X2, [p1d[z] for z in X2.tolist()], 'b', linewidth=5)
        ax0.set_title("1D polyfit; order 3")

        ax1 = fig.add_subplot(2, 2, 1, projection='3d')

        surf = ax1.plot_surface(X, Y, Z2, rstride=1, cstride=1,
                                cmap=cm.coolwarm,
                                linewidth=0, antialiased=False)
        ax1.scatter(X, Y, Z, c='r', marker='^')
        ax1.set_zlim(-5.01, 5.01)
        ax1.set_title("fitted surface PolyFit2D")

        ax1.zaxis.set_major_locator(LinearLocator(10))
        ax1.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        ax2 = fig.add_subplot(2, 2, 3, projection='3d')

        surf = ax2.plot_surface(X, Y, Z3, rstride=1, cstride=1,
                                cmap=cm.coolwarm, linewidth=0,
                                antialiased=False)
        ax2.scatter(X, Y, Z, c='r', marker='^')
        ax2.set_zlim(-5.01, 5.01)
        ax2.set_title("fitted surface PolyFitND")

        ax2.zaxis.set_major_locator(LinearLocator(10))
        ax2.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # fig.colorbar(surf, aspect=1)
        plt.show()

    except ImportError:

        print("cannot demonstrate use for surfaces, no matplotlib found.\n"
              "Note, however, this is not required for using this script.\n"
              "Only needed for demonstrations.")

    except:
        try:
            import traceback

            tb = traceback.format_exc()
            print(tb)
        except:
            pass
