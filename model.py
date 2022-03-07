from symtable import Symbol
import control as clt
from sympy import *

class SystemControl:
    num = 4
    den = [1, 2, 0]
    sys = clt.tf(num, den)

class FunctionSystem:
    s = Symbol('s')
    Gs = 4 / (s * (s + 2))





