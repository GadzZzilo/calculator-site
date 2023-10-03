from django.shortcuts import render
from django.views.generic import ListView
from sympy import Symbol, integrate

#logic


def indefinite_integral(given):
    var = Symbol('x')
    res = str(integrate(given, var)) + ' + C'
    if 'log' in res:
        res = res.replace('log', 'ln')
    return res
#########################


def home(request):
    context = {}
    if request.method == 'POST':
        data = request.POST['given']

        if 'btn1' in request.POST:
            res = indefinite_integral(data)
            context['result'] = res
            return render(request, 'index.html', context)
    return render(request, 'index.html')

