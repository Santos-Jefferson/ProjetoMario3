import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
import flopy
import pandas as pd
from helpers import PlotT1, PlotT2, PlotT2I, PlotT3, DisIrregurlar, readSingleRowTG, convert_array, get_water_table, \
    get_gradients, get_saturated_thickness

# Aqui é onde vai a base de dados, o diretorio dos arquivos
os.chdir('Documents/')
directorio_actual = os.getcwd()
carpeta = Path(directorio_actual)
BD_ws = carpeta/'BD.db'

# Aqui é onde vai o input
numceldasi = 10  # tiene que ser numeros pares
numLayi = numLayf = 10
topRef = 100  # Superficie do solo
botRef = 50  # Profundidade de solo
G = 0  #
h1 = 100  #
hk = 1  #
vk = (hk / 10)
Caudal = 1  # Caudal en litros/segundo #

ArrayEsp = [10, 30, 60, 90, 120]

# Aqui é input pra um grafico
# Grafica para la capa deseada con la exageracion vertical deseada las diferentes condiciones simuladas en I1
Capa = 10
ExagVert = 1000
PlotT1(BD_ws, hk, G, Caudal, ArrayEsp, Capa, ExagVert, topRef)

# Grafica para la capa deseada con la exageracion vertical deseada en un recuadro deseado enmarcado por Xmin, Xmax, Ymin
# las curva de mayor espaciamento 'a', la de menor espaciamento 'b' y la de distribucion irregular 'i'
Capa = 10
ExagVert = 1000
Xmin = 0.9;
Xmax = 1  # 0-1 Fraccion de la longitud total
Ymin = 0  # 0-1 Fraccion del abatimiento total
(x2_a, x2_b, x2_i, CiH_a, CiH_b, CiH_i, fig2) = PlotT2(BD_ws, hk, G, Caudal, ArrayEsp, Capa, ExagVert, Xmin, Xmax, Ymin,
                                                 topRef)

# Calcula las distribucion irregular de espaciamento de celda optimo
(A, D) = DisIrregurlar(BD_ws, G, Caudal, hk)  # Isso terá que ser vizualizado no site
print(D)

# --------------------------------------------------

# Opciones Graficas para el modelo con distribucion irregular de celdas
Capa = 1
PlotT2I(BD_ws, hk, G, Caudal, Capa, D, carpeta)

# Colocar mais inputs nessas informações

Capa = 1  #
C = 9  #
F = 5  #
P = 50  #
ExagVert = 100
Xmin = 1;
Xmax = 11161
# Xmin = 4000; Xmax =7000 # 0-1 Fraccion de la longitud total
Ymin = 80  # 0-1 Fraccion del abatimiento total
DeltaPlot = 0.1
PlotT3(BD_ws, hk, G, Caudal, ArrayEsp, Capa, C, F, P, ExagVert, Xmin, Xmax, topRef, DeltaPlot)

Capa = 1
C = 9
F = 5
P = 28
ExagVert = 1
# Xmin = 1; Xmax =11161
Xmin = 5450;
Xmax = 5700  # 0-1 Fraccion de la longitud total
Ymin = 80  # 0-1 Fraccion del abatimiento total
DeltaPlot = 0.1

PlotT3(BD_ws, hk, G, Caudal, ArrayEsp, Capa, C, F, P, ExagVert, Xmin, Xmax, topRef, DeltaPlot)

Capa = 1
C = 9
F = 5
P = 17
ExagVert = 10
# Xmin = 1; Xmax =11161
Xmin = 5100;
Xmax = 6100  # 0-1 Fraccion de la longitud total
Ymin = 80  # 0-1 Fraccion del abatimiento total
DeltaPlot = 0.1
PlotT3(BD_ws, hk, G, Caudal, ArrayEsp, Capa, C, F, P, ExagVert, Xmin, Xmax, topRef, DeltaPlot)

# Outro botão para pular as imagens
# Daqui pra frente as funçoes serao juntas para apresentar as imagens
Capa = 1
C = 9
F = 5
P = 15

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
model_ws = os.path.join(carpeta/'Model/')
model_name = 'ex'
lst = flopy.utils.Mf6ListBudget(os.path.join(model_ws, model_name + ".lst"))  # Arquivo de texto
cumulative = lst.get_budget()

df = lst.get_dataframes(diff=True)[0]
ax = df.plot(kind="bar", figsize=(6, 6))
ax.set_xticklabels(["historic", "scenario"])
plt.show()

incrementaldf, cumulativedf = lst.get_dataframes()
incrementaldf
