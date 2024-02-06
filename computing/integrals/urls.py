from django.urls import path

from . import views

urlpatterns = [
    path('', views.indefinite_integral, name='index'),  # должен быть автоматический переход на неопределенный интеграл
    path("Неопределенный_интеграл/", views.indefinite_integral, name="indefinite_integral"),
    path("Определенный_интеграл/", views.definite_integral, name="definite_integral"),
]
