from django.urls import path

from . import views

urlpatterns = [
    path('input_graficos01/', views.input_graficos01, name='input_graficos01'),
    path('input_graficos02/', views.input_graficos02, name='input_graficos02'),
    path('graficos01/', views.graficos01, name='graficos01'),
    path('graficos02/', views.graficos02, name='graficos02'),
    path('', views.index, name='index'),
]
