from django.shortcuts import render


from .calculation import *


def indefinite_integral(request):
    context = {}
    if request.method == "POST" and request.POST["given"] and "btn1" in request.POST:
        context["given"] = request.POST["given"]
        context["var"] = request.POST["var"]
        context = calculate_indefinite_integral(context)

        return render(request, "indefinite_integral.html", context=context)
    return render(request, "indefinite_integral.html")


def definite_integral(request):
    context = {}
    if request.method == "POST" and request.POST["given"] and "btn1" in request.POST:
        context["given"] = request.POST["given"]
        context["var"] = request.POST["var"]
        context["low_lim"] = request.POST["low_lim"]
        context["up_lim"] = request.POST["up_lim"]
        calculate_definite_integral(context)
        return render(request, "definite_integral.html", context=context)

    return render(request, "definite_integral.html")


def index(request):
    return render(request, 'base.html')
