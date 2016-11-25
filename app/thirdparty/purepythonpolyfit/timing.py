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
This file evaluates the timings of the single method in the 
purePythonPolyFit.py module
"""

# sys imports
import sys
from inspect import isfunction
import numpy as np
from functools import wraps
from time import clock

# my imports
import purePythonPolyFit as PPP
#from purePythonPolyFit import *

times = {}
currentCallStack = []


def timed(f):
    """
    measure the clock time of functions as well as the pure times,
    without the subfunction calls
    (However, the latter is not as accurate since it includes some management
     of the timing)
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        startOverall = clock()
        global currentCallStack
        global times
        name = f.__name__
        currentCallStack.append(name)
        if name not in times:
            times[name] = {"numCalls": 0, "totalTime": 0, "subprocesses": 0, "numSub" : 0}
        start = clock()
        result = f(*args, **kwds)
        elapsed = clock() - start
        currentCallStack = currentCallStack[:-1]
        times[name]["numCalls"] += 1
        times[name]["totalTime"] += elapsed
        if len(currentCallStack) > 1:
            times[currentCallStack[-2]]["numSub"] += 1
            times[currentCallStack[-2]]["subprocesses"] += clock() - startOverall
        return result
    return wrapper    

def printTimes():
    """
    pretty print timing results
    """
    global times
    # determine maximum length:
    header = "function name"
    ma = len(header)
    sum = 0
    sumOverall = 0
    for name, ts in times.items():
        ma = max(ma, len(name))
        net = (ts['totalTime'] - ts['subprocesses'])/float(ts['numCalls'])
        sum += net
        sumOverall += (ts['totalTime'] - ts['subprocesses'])
    ma += 2
                 
    print("\033[1moverall (mean) processor time\033[0m: %0.5fs (%0.5fs)" %(sumOverall, sum))
    print("listing processor time per method:" )
    print("\033[1m%s%s\t %% Overall time\t Mean w.o. Sub[s]\t  Mean[s]\tNum-Calls\033[0m" % (header, ' '*(ma - len(header))))
    for name in sorted(times.keys()):
        ts = times[name]
        m = ts['totalTime']/float(ts['numCalls'])
        net = (ts['totalTime'] - ts['subprocesses'])/float(ts['numCalls'])
        perc = 100.0*net/float(sum)
        print("%s%s\t% 15.2f\t% 17.5f\t% 9.5f\t% 9d" %(name,
                                                ' '*(ma - len(name)),
                                                        perc,
                                                net,
                                                m,

                                                       ts['numCalls']))

from array import array
import copy
if __name__ == "__main__":
    
    fnLists = [x for x in dir(PPP) if isfunction(eval('PPP.%s' % x))]

    
    PPP.elementWise = timed(PPP.elementWise)
    PPP.eyeMatrix = timed(PPP.eyeMatrix)
    PPP.leastSquareSolution = timed(PPP.leastSquareSolution)
    PPP.matrixMultiplication = timed(PPP.matrixMultiplication)
    PPP.mean = timed(PPP.mean)
    PPP.meanAndStandardDeviation = timed(PPP.meanAndStandardDeviation)
    PPP.norm = timed(PPP.norm)
    PPP.qr = timed(PPP.qr)
    PPP.solveWithBackwardReplacement = timed(PPP.solveWithBackwardReplacement)
    PPP.solveWithForwardReplacement = timed(PPP.solveWithForwardReplacement)
    PPP.transpose = timed(PPP.transpose)
    PPP.PolyFit.__init__ = timed(PPP.PolyFit.__init__)
    PPP.PolyFit2D.__init__ = timed(PPP.PolyFit2D.__init__)
    PPP.PolyFitND.__init__ = timed(PPP.PolyFitND.__init__)    

    times = {}
    n = 40
    print("\nPolyFit times (n=%d):" % n)
    for i in range(2):
        pts = np.random.randn(n).tolist()
        vals = np.random.randn(n).tolist()
        for i in range(5):
            p = PPP.PolyFit(pts, vals, order = 5)
    printTimes()

    n = 40
    print("\n\nPolyFit2D times (n=%d):" % n)
    times = {}
    for i in range(2):
        pts = np.random.randn(n,2).tolist()
        vals = np.random.randn(n).tolist()
        for i in range(5):
            p = PPP.PolyFit2D(pts, vals, order = 5)
    printTimes()

    n = 10
    print("\n\nPolyFitND times for 5D (n=%d):"%n)
    times = {}
    for i in range(2):
        pts = np.random.randn(n,5).tolist()
        vals = np.random.randn(n).tolist()
        for i in range(5):
            p = PPP.PolyFitND(pts, vals, order = 5)
    printTimes()               
    
    times = {}
    mats = [(np.random.randn(30,50).tolist(), np.random.randn(50, 12).tolist()),
            (np.random.randn(40,40).tolist(), np.random.randn(40, 40).tolist()),
            (np.random.randn(50,30).tolist(), np.random.randn(30, 45).tolist())]
    for i in range(100):
        for m in mats:
            res = PPP.matrixMultiplication(m[0], m[1])
    printTimes()
