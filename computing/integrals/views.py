import sympy
import sympy as sp
from django.shortcuts import render
from django.views.generic import ListView
from matplotlib import pyplot as plt
from sympy import Symbol, integrate
import numpy as np
from io import BytesIO
import base64
import matplotlib as mpl


def indefinite_integral(request):
    context = {}
    if request.method == "POST" and request.POST["given"] and "btn1" in request.POST:
        sym = Symbol(str(request.POST["var"]))
        res = str(integrate(request.POST["given"], sym)) + ' + C'

        if 'log' in res:
            res = res.replace('log', 'ln')

        plot = create_graph(str(request.POST["given"]), res[:-4], sym)

        context["given"] = request.POST["given"]
        context["result"] = res
        context["plot"] = plot
        return render(request, "indefinite_integral.html", context=context)
    return render(request, "indefinite_integral.html")


def definite_integral(request):
    context = {}
    if request.method == "POST" and request.POST["given"] and "btn1" in request.POST:
        sym = Symbol(str(request.POST["var"]))
        indefinite_res = str(integrate(request.POST["given"], sym)) + " + C"
        res = str(integrate(request.POST["given"], (sym, request.POST["low_lim"], request.POST["up_lim"])))

        if 'log' in indefinite_res:
            res = res.replace('log', 'ln')

        plot = create_graph(
            str(request.POST["given"]),
            indefinite_res[:-4],
            sym,
            float(request.POST["low_lim"]),
            float(request.POST["up_lim"])
        )

        context["given"] = request.POST["given"]
        context["result"] = indefinite_res + " = " + res
        return render(request, "definite_integral.html", context=context)
    return render(request, "definite_integral.html")


def create_graph(
        func_1: str,
        func_2: str,
        symbol: sympy.core.symbol.Symbol,
        low_border: float = -50,
        up_border: float = 50
):
    abscissa_values = np.linspace(low_border, up_border, 50)
    func_1 = sp.sympify(func_1)
    func_2 = sp.sympify(func_2)
    mpl.use("agg")

    ordinate_values_1 = [func_1.subs(symbol, val) for val in abscissa_values]
    ordinate_values_2 = [func_2.subs(symbol, val) for val in abscissa_values]

    plt.plot(abscissa_values, ordinate_values_1, color="b", label="f(x)")
    plt.plot(abscissa_values, ordinate_values_2, color="g", label="F(x)")
    plt.xlabel(str(symbol))
    plt.ylabel("y")
    plt.title(f"Графики функций")
    plt.grid()
    plt.legend()

    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    encoded_img = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return encoded_img


def index(request):
    return render(request, 'base.html')
