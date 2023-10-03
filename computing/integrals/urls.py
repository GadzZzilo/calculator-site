from django.urls import path

from . import views

urlpatterns = [
    path('', views.compute_integral, name='integrals'),
]
