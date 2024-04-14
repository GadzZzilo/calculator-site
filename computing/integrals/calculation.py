import copy
import sympy
import sympy as sp
import numpy as np
from io import BytesIO
import base64
import matplotlib as mpl
from matplotlib import pyplot as plt
from sympy import Symbol, integrate, S


def redo_root(given):
    res = given.replace("sqrt", "√")
    return res


def redo_pi(given):
    res = given.replace("pi", "π")
    return res


def redo_ln(given):
    res = given.replace("log", "ln")
    return res


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


def create_graph(
        func_1: str,
        func_2: str,
        symbol: sympy.core.symbol.Symbol,
        low_border: float = -50,
        up_border: float = 50
):
    abscissa_values = np.linspace(low_border, up_border, 400)
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


def redo_indefinite_integral(res):
    if "Integral" in res:
        res = "Недостаточно возможностей для нахождения первообразной данного интеграла"
    if "sqrt" in res:
        res = redo_root(res)
    if "pi" in res:
        res = redo_pi(res)
    if "log" in res:
        res = redo_ln(res)

    return res


def redo_definite_integral(res, indefinite_res):
    if res == "nan":
        res = "Не определено"
    if "Integral" in indefinite_res:
        indefinite_res = "Недостаточно возможностей для нахождения первообразной данного интеграла"
    if "sqrt" in indefinite_res:
        indefinite_res = redo_root(indefinite_res)
        res = redo_root(res)
    if "pi" in indefinite_res:
        indefinite_res = redo_pi(indefinite_res)
        res = redo_pi(res)
    if "log" in indefinite_res:
        indefinite_res = redo_ln(indefinite_res)
        res = redo_ln(res)

    return indefinite_res, res


def calculate_indefinite_integral(context):
    sym = Symbol(context["var"])
    if "log" in context["given"]:
        context["given"] = redo_log(context["given"])

    try:
        res = str(integrate(context["given"], sym)) + ' + C'

        try:
            plot = create_graph(context["given"], res[:-4], sym)
            context["plot"] = plot
        except Exception as ex:
            print(ex)

        context["result"] = redo_indefinite_integral(res)

    except Exception as ex:
        print(ex)


def calculate_definite_integral(context):
    sym = Symbol(context["var"])
    low_lim = context["low_lim"] if context["low_lim"] != "" and context["low_lim"] != "-∞" else -S.Infinity
    up_lim = context["up_lim"] if context["up_lim"] != "" and context["up_lim"] != "+∞" else S.Infinity

    if "log" in context["given"]:
        context["given"] = redo_log(context["given"])

    try:
        indefinite_res = str(integrate(context["given"], sym)) + " + C"
        res = str(integrate(context["given"], (sym, low_lim, up_lim)))

        try:
            plot = create_graph(
                str(context["given"]),
                indefinite_res[:-4],
                sym,
                float(context["low_lim"] if low_lim != -S.Infinity else -50),
                float(context["up_lim"] if up_lim != S.Infinity else 50)
            )
            context["plot"] = plot
        except Exception as ex:
            print(ex)

        indefinite_res, res = redo_definite_integral(res, indefinite_res)

        context["result"] = f"{indefinite_res}{' = ' + res if 'Не' not in indefinite_res and 'Не' not in res else ''}"
    except Exception as ex:
        print(ex)

