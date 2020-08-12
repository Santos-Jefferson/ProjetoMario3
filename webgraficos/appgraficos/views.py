import sys
from webgraficos.settings import BASE_DIR
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PaginaInputForm, Plot3InputForm
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
import flopy
import pandas as pd
from .helpers import PlotT1, PlotT2, PlotT2I, PlotT3, DisIrregurlar, readSingleRowTG, convert_array, get_water_table, \
    get_gradients, get_saturated_thickness

# Aqui é onde vai a base de dados, o diretorio dos arquivos
print(BASE_DIR)
os.chdir(os.path.join(BASE_DIR, 'appgraficos\Documents'))
directorio_actual = os.getcwd()
print(directorio_actual)
carpeta = directorio_actual
print(carpeta)
BD_ws = os.path.join(carpeta, 'BD.db')
print(BD_ws)
ArrayEsp = [10, 30, 60, 90, 120]


def index(request):
    if request.method == 'POST':
        form = PaginaInputForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('appgraficos/resultados.html')
    else:
        form = PaginaInputForm()

    return render(request, 'appgraficos/index.html', {'form': form})


def input_plot3(request):
    if request.method == 'POST':
        form = Plot3InputForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('appgraficos/graficos_plot3.html')
    else:
        form = Plot3InputForm()

    return render(request, 'appgraficos/input_plot3.html', {'form': form})


def resultados(request):
    if request.method == 'POST':
        form = request.POST

    # Aqui é onde vai o input
    numceldasi = int(form['numceldasi'])  # tiene que ser numeros pares
    numLayi = numLayf = int(form['numlayi'])
    topRef = int(form['topref'])  # Superficie do solo
    botRef = int(form['botref'])  # Profundidade de solo
    G = int(form['g'])  #
    h1 = int(form['h1'])  #
    hk = int(form['hk'])  #
    vk = hk / 10
    Caudal = int(form['caudal'])  # Caudal en litros/segundo #



    # Aqui é input pra um grafico
    # Grafica para la capa deseada con la exageracion vertical deseada las diferentes condiciones simuladas en I1
    Capa = 10
    ExagVert = 1000
    PlotT1(BD_ws, hk, G, Caudal, ArrayEsp, Capa, ExagVert, topRef)

    # Grafica para la capa deseada con la exageracion vertical deseada en un recuadro deseado enmarcado por Xmin, Xmax, Ymin
    # las curva de mayor espaciamento 'a', la de menor espaciamento 'b' y la de distribucion irregular 'i'
    Capa = 10
    ExagVert = 1000
    Xmin = 0.9
    Xmax = 1  # 0-1 Fraccion de la longitud total
    Ymin = 0  # 0-1 Fraccion del abatimiento total
    (x2_a, x2_b, x2_i, CiH_a, CiH_b, CiH_i) = PlotT2(BD_ws, hk, G, Caudal, ArrayEsp, Capa, ExagVert, Xmin, Xmax, Ymin,
                                                     topRef)

    # Calcula las distribucion irregular de espaciamento de celda optimo
    (A, D) = DisIrregurlar(BD_ws, G, Caudal, hk)  # Isso terá que ser vizualizado no site
    print(D)

    # --------------------------------------------------

    # Opciones Graficas para el modelo con distribucion irregular de celdas
    Capa = 1
    fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9 = PlotT2I(BD_ws, hk, G, Caudal, Capa, D, carpeta)

    figuras = {
        'fig1': fig1,
        'fig2': fig2,
        'fig3': fig3,
        'fig4': fig4,
        'fig5': fig5,
        'fig6': fig6,
        'fig7': fig7,
        'fig8': fig8,
        'fig9': fig9,
    }

    return render(request, 'appgraficos/resultados.html', figuras)


def graficos_plot3(request):
    if request.method == 'POST':
        form = request.POST

    # Aqui é onde vai o input
    hk = int(form['hk'])  #
    G = int(form['g'])  #
    Caudal = int(form['caudal'])  # Caudal en litros/segundo #
    topRef = int(form['topref'])  # Superficie do solo


    Capa = int(form['capa1'])
    C = int(form['c1'])
    F = int(form['f1'])
    P = int(form['p1'])
    ExagVert = int(form['exagvert1'])
    Xmin = int(form['xmin1'])
    Xmax = int(form['xmax1'])
    Ymin = int(form['ymin1'])
    DeltaPlot = float(form['deltaplot1'])

    fig10 = PlotT3(BD_ws, hk, G, Caudal, ArrayEsp, Capa, C, F, P, ExagVert, Xmin, Xmax, topRef, DeltaPlot)

    Capa = int(form['capa2'])
    C = int(form['c2'])
    F = int(form['f2'])
    P = int(form['p2'])
    ExagVert = int(form['exagvert2'])
    Xmin = int(form['xmin2'])
    Xmax = int(form['xmax2'])
    Ymin = int(form['ymin2'])
    DeltaPlot = float(form['deltaplot2'])

    fig11 = PlotT3(BD_ws, hk, G, Caudal, ArrayEsp, Capa, C, F, P, ExagVert, Xmin, Xmax, topRef, DeltaPlot)

    Capa = int(form['capa3'])
    C = int(form['c3'])
    F = int(form['f3'])
    P = int(form['p3'])
    ExagVert = int(form['exagvert3'])
    Xmin = int(form['xmin3'])
    Xmax = int(form['xmax3'])
    Ymin = int(form['ymin3'])
    DeltaPlot = float(form['deltaplot3'])

    fig12 = PlotT3(BD_ws, hk, G, Caudal, ArrayEsp, Capa, C, F, P, ExagVert, Xmin, Xmax, topRef, DeltaPlot)

    # Outro botão para pular as imagens
    # Daqui pra frente as funçoes serao juntas para apresentar as imagens

    Capa = int(form['capa4'])
    C = int(form['c4'])
    F = int(form['f4'])
    P = int(form['p4'])

    Table = 'G{}Q{}KI'.format(G, Caudal)
    Id = 'K{}I'.format(hk)
    RecordD = readSingleRowTG(BD_ws, Table, Id)
    xd = convert_array(RecordD[2])
    Xt = np.array(list(it.accumulate(xd)))
    x = Xt[:]
    z = np.linspace(topRef - 0.5, topRef - P + 0.5, P)

    Table = 'resp3G{}Q{}KIP'.format(G, Caudal)
    Id = 'K{}C{}F{}P{}'.format(hk, C, F, P)
    RecordH = readSingleRowTG(BD_ws, Table, Id)
    h = convert_array(RecordH[5])
    H = np.where(h < 0, 0, h)
    HminC1 = H != 0
    HminC2 = H[HminC1]

    fig = plt.figure(figsize=(15, 15))
    wt = get_water_table(H, per_idx=None)
    plt.imshow(wt)
    plt.colorbar(label='Elevation');

    Table = 'G{}Q{}KI'.format(G, Caudal)
    Id = 'K{}I'.format(hk)
    Record = readSingleRowTG(BD_ws, Table, Id)
    h = convert_array(Record[15])
    hmin = np.ma.round(h[Capa - 1].min(), decimals=1)
    hmax = np.ma.round(h[Capa - 1].max(), decimals=1)
    Fitcolor = (hmax - hmin) * 0.8 + hmin

    grad, unsat, hds, zcnt_per, dz, dh = get_gradients(h, topRef, nodata=-999)
    # fig = plt.figure(figsize=(15,15))
    # ax = plt.gca()

    fig, axes = plt.subplots(3, 3, figsize=(11, 8.5))
    axes = axes.flat

    for i, vertical_gradient in enumerate(grad):
        im = axes[i].imshow(vertical_gradient, vmin=grad.min(), vmax=grad.max())
        axes[i].set_title('Vertical gradient\nbetween Layers {} and {}'.format(i + 1, i + 2))
        ctr = axes[i].contour(vertical_gradient, levels=[-.1, -.05, 0., .05, .1],
                              colors='k', linewidths=0.5)
        plt.clabel(ctr, fontsize=8, inline=1)

    fig.subplots_adjust(right=.8)
    fig.subplots_adjust(top=1.1)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])
    fig.colorbar(im, cax=cbar_ax, label='positive downward');

    pd.options.display.float_format = '{:.3f}'.format
    df2 = pd.DataFrame(data=dh[0])

    st = get_saturated_thickness(H, topRef, per_idx=None)
    fig = plt.figure(figsize=(15, 15))
    plt.imshow(st)
    plt.colorbar(label='Saturated thickness')
    plt.title('Layer 1');

    # Arquivos de texto, extensão do flopy, colocar meu novo roteiro
    model_ws = os.path.join(carpeta, 'Model')
    model_name = 'ex'
    lst = flopy.utils.Mf6ListBudget(os.path.join(model_ws, model_name + ".lst"))  # Arquivo de texto
    cumulative = lst.get_budget()

    df = lst.get_dataframes(diff=True)[0]
    ax = df.plot(kind="bar", figsize=(6, 6))
    ax.set_xticklabels(["historic", "scenario"])
    # plt.show()

    incrementaldf, cumulativedf = lst.get_dataframes()
    incrementaldf

    figuras = {
        'fig10': fig10,
        'fig11': fig11,
        'fig12': fig12,
    }

    return render(request, 'appgraficos/graficos_plot3.html', figuras)
