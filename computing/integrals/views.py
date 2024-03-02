import copy

import sympy
import sympy as sp
from django.shortcuts import render
from matplotlib import pyplot as plt
from sympy import Symbol, integrate, S
import numpy as np
from io import BytesIO
import base64
import matplotlib as mpl


def redo_log(given: str):
    log_num = given.count("log")
    start_ind = given.find("log")
    data = []
    given_ind = copy.copy(given)

    for log_ind in range(log_num):
        for ind, el in enumerate(given_ind[start_ind + 3:]):
            if el == "(":
                end_base_ind = ind
                log_key = f"{given_ind[start_ind:start_ind + 3 + end_base_ind]}"
                base = given_ind[start_ind + 3:start_ind + 3 + end_base_ind]
                data.append({"base": base, "log_key": log_key})

                given_ind = given_ind.replace("log", "ppp", 1)
                start_ind = given_ind.find("log")
                break

    for ind_log_dict, log_dict in enumerate(data):
        open_bracket = 0
        close_bracket = 0
        start_expression_ind = 0
        start_ind = given.find(log_dict["log_key"])

        for ind, el in enumerate(given[start_ind + 3:]):
            if el == "(":
                open_bracket += 1

                if open_bracket == 1:
                    start_expression_ind = ind + 1

            elif el == ")":
                close_bracket += 1

                if open_bracket == close_bracket:
                    end_expression_ind = ind
                    data[ind_log_dict]["expression"] = given[start_ind + 3:][start_expression_ind:end_expression_ind]
                    end_ind = ind + start_ind + 4
                    given = given[:start_ind] + f"log({data[ind_log_dict]['expression']}, {data[ind_log_dict]['base']})" + given[end_ind:]
                    break

    return given


def indefinite_integral(request):
    context = {}
    if request.method == "POST" and request.POST["given"] and "btn1" in request.POST:
        context["given"] = request.POST["given"]
        sym = Symbol(str(request.POST["var"]))

        if "log" in context["given"]:
            context["given"] = redo_log(context["given"])

        try:
            res = str(integrate(context["given"], sym)) + ' + C'
        except Exception as ex:
            print(ex)

        try:
            plot = create_graph(context["given"], res[:-4], sym)
            context["plot"] = plot
        except Exception as ex:
            print(ex)

        context["result"] = res
        return render(request, "indefinite_integral.html", context=context)
    return render(request, "indefinite_integral.html")


def definite_integral(request):
    context = {}
    if request.method == "POST" and request.POST["given"] and "btn1" in request.POST:
        context["given"] = request.POST["given"]
        sym = Symbol(str(request.POST["var"]))
        indefinite_res = str(integrate(context["given"], sym)) + " + C"
        low_lim = request.POST["low_lim"] if request.POST["low_lim"] else -S.Infinity
        up_lim = request.POST["up_lim"] if request.POST["up_lim"] else S.Infinity

        if "log" in context["given"]:
            context["given"] = redo_log(context["given"])

        try:
            res = str(integrate(context["given"], (sym, low_lim, up_lim)))

            if res == "nan" or "Integral" in res:
                res = "Не определено"

            context["result"] = f"{indefinite_res}{' = ' + res if res != 'Не определено' else ''}"
        except Exception as ex:
            print(ex)

        try:
            plot = create_graph(
                str(context["given"]),
                indefinite_res[:-4],
                sym,
                float(request.POST["low_lim"] if low_lim != -S.Infinity else -50),
                float(request.POST["up_lim"] if up_lim != S.Infinity else 50)
            )
            context["plot"] = plot
        except Exception as ex:
            print(ex)

        return render(request, "definite_integral.html", context=context)
    return render(request, "definite_integral.html")


def create_graph(
        func_1: str,
        func_2: str,
        symbol: sympy.core.symbol.Symbol,
        low_border: float = -50,
        up_border: float = 50
):
    abscissa_values = np.linspace(low_border, up_border, 100)
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
