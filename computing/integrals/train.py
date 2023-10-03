from sympy import Symbol, integrate


def indefinite_integral(given):
    var = Symbol('x')
    res = integrate(given, var)
    return res

if __name__ == '__main__':
    print(indefinite_integral('x **2'))
