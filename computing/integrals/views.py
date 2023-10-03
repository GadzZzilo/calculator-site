from django.shortcuts import render
from django.views.generic import ListView
from sympy import Symbol, integrate

#logic


def indefinite_integral(given, var):
    sym = Symbol(str(var))
    res = str(integrate(given, sym)) + ' + C'
    if 'log' in res:
        res = res.replace('log', 'ln')
    return res
#########################


def compute_integral(request):
    context = {}
    if request.method == 'POST':
        data = request.POST['given']
        context['given'] = data

        if 'btn1' in request.POST:
            var = request.POST['var']
            res = indefinite_integral(data, var)
            context['result'] = res
            return render(request, 'base.html', context)
    return render(request, 'base.html')
