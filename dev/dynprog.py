# Implementation of DynProg in 2005 GHJM
import numpy as np

expression = lambda x : ((x[0] or x[1]) and (x[2] or x[3] or x[4] or x[5] or x[6])) or (x[7] or x[8])
expression = "(x0 and x1) or (x2 or x3)"
expression = "((x0 or x1) and (x2 or x3 or x4 or x5 or x6)) or x7 or x8"

def resolved(expression, xL, gate):
    splitted = expression.split(gate)
    for term in splitted:
        if "x"+str(xL) in term and "x"+str(xL+1) in term:
            return True
    return False

def resolve(expression, L, sclasses, condition):
    for i in sclasses[L]:
        expression = expression.replace("x"+str(i), condition)
    return expression

sclasses = [[0,1], [2,3]] # sibling-classes
sclasses = [[0,1], [2,3,4,5,6],[7,8]] # sibling-classes
T = [2, 2]
T = [0,1,1]
dtuple = T
expressions = {}
for L in range(len(sclasses)):
    xL = sclasses[L][-dtuple[L]] # 0
    ILp = expression.replace("x"+str(xL), "True")
    if T[L] == 1 or resolved(expression, xL, "and"):
        ILptuple = tuple(T[:L] + [0] + T[(L+1):])
        ILmexpression = resolve(expression, L, sclasses, "True")
        print(ILmexpression)
    else: 
        ILptuple = tuple(T[:L] + [T[L]-1] + T[(L+1):])
    ILm = expression.replace("x"+str(xL), "False")
    if T[L] == 1 or resolved(expression, xL, "or"):
        ILmtuple = tuple(T[:L] + [0] + T[(L+1):])
    else: 
        ILmtuple = tuple(T[:L] + [T[L]-1] + T[(L+1):])
    print(xL)
    print(ILp)
    print(ILptuple)
    print(ILm)
    print(ILmtuple)
    print()
