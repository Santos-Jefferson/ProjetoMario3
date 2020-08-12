from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input_plot3/', views.input_plot3, name='input_plot3'),
    path('resultados/', views.resultados, name='resultados'),
    path('graficos_plot3/', views.graficos_plot3, name='graficos_plot3'),

]
