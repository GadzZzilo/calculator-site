import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol
import sympy as sp


def create_graph(func_str, symbol, low_border=-50, up_border=50):
    abscissa_values = np.linspace(low_border, up_border, 100)
    func = sp.sympify(func_str)

    ordinate_values = [func.subs(symbol, val) for val in abscissa_values]

    plt.plot(abscissa_values, ordinate_values)

    plt.xlabel(str(symbol))
    plt.ylabel(f"f({str(symbol)})")
    plt.title(f"График функции f = {func_str}")

    filename = "integral_plot.png"
    plt.savefig(f"{filename}")


create_graph("0.5*x^3 + 4*x", Symbol("x"))