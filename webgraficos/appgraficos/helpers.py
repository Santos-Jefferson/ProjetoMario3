import os
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from matplotlib import cm
import sqlite3
import io
import numpy as np
import itertools as it
from flopy.discretization.structuredgrid import StructuredGrid


# Este é um grafico
def PlotT1(BD_ws, hk, G, Caudal, ArrayEsp, Capa, ExagVert, topref):
    fig = plt.figure(figsize=(10, 10))

    MinArray = []
    LongDist = []
    NC = []
    Table = 'G{}Q{}KU'.format(G, Caudal)
    Idf = 'K{}U{}'.format(hk, ArrayEsp[len(ArrayEsp) - 1])
    Recordf = readSingleRowTG(BD_ws, Table, Idf)
    HEADSescf = convert_array(Recordf[7])
    CiHf = HEADSescf[len(HEADSescf) - 1]
    MaxL = len(CiHf) * ArrayEsp[len(ArrayEsp) - 1]

    for i in range(len(ArrayEsp)):
        Id = 'K{}U{}'.format(hk, ArrayEsp[i])

        Record = readSingleRowTG(BD_ws, Table, Id)
        HEADSesc = convert_array(Record[7])
        CiH = HEADSesc[Capa - 1]

        MinArrayFin = np.ma.round(np.amin(CiH), decimals=2)
        MinArray.append(MinArrayFin)

        Xn = len(CiH)
        delcol = ArrayEsp[i]
        longitud = Xn * delcol
        LongDist.append(longitud)
        NC.append(Xn)
        x2 = np.linspace((MaxL - Xn * ArrayEsp[i]), MaxL, Xn)

        xmin, xmax, ymin, ymax = plt.axis([0, MaxL, np.amin(MinArray) * 0.995, topref])
        ax = plt.gca()
        t = ax.set_title('''Capa = {},  Esp Celda: {},  ncol: {}  
        Longitud: {},  Hmin: {}'''.format(Capa, ArrayEsp, NC, LongDist, MinArray))
        ax.set_aspect(ExagVert)
        plt.plot(x2, CiH)
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        fig1 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        return fig1


def readSingleRowTG(BD_ws, Table, developerId):
    try:
        sqliteConnection = sqlite3.connect(BD_ws)
        cursor = sqliteConnection.cursor()

        sqlite_select_query = """SELECT * from {} where Id = ?""".format(Table)
        cursor.execute(sqlite_select_query, (developerId,))

        record = cursor.fetchone()

        return (record)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


def PlotT2(BD_ws, hk, G, Caudal, ArrayEsp, Capa, ExagVert, Xmin, Xmax, Ymin, topref):
    fig = plt.figure(figsize=(10, 10))

    Table = 'G{}Q{}KI'.format(G, Caudal)
    Id = 'K{}I'.format(hk)
    Record = readSingleRowTG(BD_ws, Table, Id)

    HEADSesc_i = convert_array(Record[6])
    HEADSesc_a = convert_array(Record[9])
    HEADSesc_b = convert_array(Record[11])
    CiH_i = HEADSesc_i[Capa - 1]
    CiH_a = HEADSesc_a[Capa - 1]
    CiH_b = HEADSesc_b[Capa - 1]

    MaxL = Record[4]
    MinArray = [np.ma.round(np.amin(CiH_a), decimals=2), np.ma.round(np.amin(CiH_b), decimals=2),
                np.ma.round(np.amin(CiH_i), decimals=2)]

    X_a = int(((Record[8] / ArrayEsp[len(ArrayEsp) - 1]) - 3) / 2)
    delcol_a = ArrayEsp[len(ArrayEsp) - 1]
    longitud = Record[8]
    X_b = int(((Record[8] / ArrayEsp[0])) / 2)
    delcol_b = ArrayEsp[0]
    X_i = len(Record[2]) / 2

    NC = [X_a, X_b, X_i]

    x2_a = np.linspace(MaxL - longitud + delcol_a * 2.5, MaxL - longitud + delcol_a * 1.5 + (X_a * delcol_a), X_a)
    x2_b = np.linspace(MaxL - longitud + delcol_b, MaxL - longitud + (X_b * delcol_b), X_b)

    R = convert_array(Record[2])
    half = int((1 + len(R)) / 2)
    C = R[:half]
    Xs = np.array(list(it.accumulate(C))) + 1
    x2_i = Xs[:-1]

    xmin, xmax, ymin, ymax = plt.axis([(MaxL - (longitud / 2)) * Xmin, (MaxL - (longitud / 2)) * Xmax,
                                       (topref - np.amin(MinArray)) * Ymin + np.amin(MinArray) * 0.995, topref])
    ax = plt.gca()
    t = ax.set_title('''Capa = {},  Esp Celda: {},  ncol: {}  
    Longitud: {},  Hmin: {}'''.format(Capa, [delcol_a, delcol_b, 'Irregular'], NC, longitud, MinArray))
    ax.set_aspect(ExagVert)
    plt.plot(x2_a, CiH_a, color='red')
    plt.plot(x2_b, CiH_b, color='blue')
    plt.plot(x2_i, CiH_i, color='green')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig2 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')

    return x2_a, x2_b, x2_i, CiH_a, CiH_b, CiH_i, fig2


def DisIrregurlar(BD_ws, G, Caudal, hk):
    serie = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 17, 20, 23, 26, 30, 35, 40, 45, 50, 55, 60, 66, 72, 78, 84, 90, 100,
             110, 120]
    Table2 = 'G{}Q{}KI'.format(G, Caudal)
    Id2 = 'K{}I'.format(hk)
    Record = readSingleRowTG2(BD_ws, Table2, Id2)
    LongDist = Record[::-1]

    SerieAcum = [90, 100, 110, 120]
    DivAcum = [420, 330, 230, 120]
    DivBloque = 330
    Intervalo = (LongDist[0] - LongDist[1]) / 2
    Array = []
    R = []

    distCelda(SerieAcum, DivAcum, DivBloque, Intervalo, R, Array, serie)

    SerieAcum = [60, 66, 72, 78, 84, 90]
    DivAcum = [450, 390, 324, 252, 174, 90]
    DivBloque = 390
    Intervalo = (LongDist[1] - LongDist[2]) / 2

    distCelda(SerieAcum, DivAcum, DivBloque, Intervalo, R, Array, serie)

    SerieAcum = [30, 35, 40, 45, 50, 55, 60]
    DivAcum = [315, 285, 250, 210, 165, 115, 60]
    DivBloque = 285
    Intervalo = (LongDist[2] - LongDist[3]) / 2

    distCelda(SerieAcum, DivAcum, DivBloque, Intervalo, R, Array, serie)

    SerieAcum = [10, 12, 14, 17, 20, 23, 26, 30]
    DivAcum = [152, 142, 130, 116, 99, 79, 56, 30]
    DivBloque = 142
    Intervalo = (LongDist[3] - LongDist[4]) / 2

    distCelda(SerieAcum, DivAcum, DivBloque, Intervalo, R, Array, serie)

    SerieAcum = [10, 10]
    DivAcum = [20, 10]
    DivBloque = 10
    Intervalo = (LongDist[4] / 2) * .8

    distCelda(SerieAcum, DivAcum, DivBloque, Intervalo, R, Array, serie)

    SerieAcum = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    DivAcum = [56, 55, 54, 52, 49, 45, 40, 34, 27, 19, 10]
    DivBloque = 55
    Intervalo = (LongDist[4] / 2) * .2

    distCelda(SerieAcum, DivAcum, DivBloque, Intervalo, R, Array, serie)

    Rf = np.sum(R)

    if Rf in serie:
        Array.append(int(Rf))
    else:
        for r in range(len(serie)):
            T = Rf - serie[len(serie) - 1 - r]
            if T > 0:
                Array.append(serie[len(serie) - 1 - r])
                Array.append(T)
                break

    A = np.sort(Array)
    B = np.array([1])
    C = A[::-1]

    C = np.append(C, B)
    D = np.append(C, A)

    return A, D


def readSingleRowTG2(BD_ws, Table, developerId):
    try:
        sqliteConnection = sqlite3.connect(BD_ws)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from {} where Id = ?""".format(Table)
        cursor.execute(sqlite_select_query, (developerId,))

        record = cursor.fetchone()
        Optimo = convert_array(record[1])

        cursor.close()

        return Optimo



    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def distCelda(SerieAcum, DivAcum, DivBloque, Intervalo, R, Array, serie):
    D = Intervalo / DivBloque
    Rd = int(D)
    Res = np.ma.round(((D - Rd) * DivBloque), decimals=0)

    '''---1er Bloque definido para intervalo mayor que el bloque de division-'''
    if Intervalo >= DivBloque:
        for i in range(1, len(SerieAcum)):
            for j in range(Rd):
                M = SerieAcum[i] * (j + 1) - SerieAcum[i] * (j)
                Array.append(M)
    '''------------------------------------'''
    '''---Si el residuo es menor que la serie analizada y es parte de la serie global--'''
    '''--Si No es parte de la serie global se guarda en una matriz R[]---'''
    if Res < np.amin(SerieAcum):
        if Res in serie:
            Array.append(int(Res))
        else:
            R.append(int(Res))
    '''------------------------------------'''
    '''--si el residuo es parte de la serie analizada--'''
    Farray = []
    Resarray = []
    Farray2 = []
    Resarray2 = []
    if Res >= np.amin(SerieAcum):
        if Res in SerieAcum:
            Array.append(int(Res))
        else:
            '''--si el residuo No es parte de la serie analizada hacer una matriz F y Resf--'''
            for i in range(len(SerieAcum)):

                F = Res / DivAcum[len(DivAcum) - 2 - i]
                Rdf = int(F)
                Resf = int((F - Rdf) * DivAcum[len(DivAcum) - 2 - i])
                F2 = Res / SerieAcum[len(SerieAcum) - 1 - i]
                Rdf2 = int(F2)
                Resf2 = int((F2 - Rdf2) * SerieAcum[len(SerieAcum) - 1 - i])

                if F >= 1:
                    Farray.append(F)

                if F2 >= 1:
                    Farray2.append(F2)

    if Farray2 != [] and Farray == []:
        fi = int(np.amin(Farray2))
        fn = int(np.amax(Farray2))

        '''--si el residuo es parte un divisor exacto de DivAcum'''
        arrayf2 = []

        for f in range(fi, fn + 1):
            ff = f / 1
            arrayf2.append(ff)

        rarray2 = []
        for r in range(len(arrayf2) - 1):
            if arrayf2[r] in Farray2:
                rarray2.append(arrayf2[r])

        if rarray2:
            rmin = np.amin(rarray2)
            IndexA = Farray2[::-1]
            Index = IndexA.index(rmin)
            Aindex = SerieAcum[Index]
            Array.append(Aindex)

            R1 = Res - Aindex

            if R1 > 0:
                if R1 in SerieAcum:
                    Array.append(int(R1))

                elif R1 < np.amin(SerieAcum):
                    R.append(int(R1))
                else:
                    for r in range(len(SerieAcum)):
                        T = R1 - SerieAcum[len(SerieAcum) - 1 - r]
                        if T > 0:
                            Array.append(SerieAcum[len(SerieAcum) - 1 - r])
                            R.append(int(T))
                            break

            '''--si el residuo "Res" esta cerca de el DivAcum que da menor residuo R1'''
        else:

            ffloat = np.amin(Farray2)
            IndexA = Farray2[::-1]
            Index = IndexA.index(ffloat)
            Aindex = SerieAcum[Index]
            Array.append(Aindex)

            R1 = Res - Aindex

            if R1 > 0:
                if R1 in SerieAcum:
                    Array.append(int(R1))

                elif R1 < np.amin(SerieAcum):
                    R.append(int(R1))
                else:
                    for r in range(len(SerieAcum)):
                        T = R1 - SerieAcum[len(SerieAcum) - 1 - r]
                        if T > 0:
                            Array.append(SerieAcum[len(SerieAcum) - 1 - r])
                            R.append(int(T))
                            break

    if Farray != []:
        fi = int(np.amin(Farray))
        fn = int(np.amax(Farray))
        '''--si el residuo es parte un divisor exacto de DivAcum'''
        arrayf = []

        for f in range(fi, fn + 1):
            ff = f / 1
            arrayf.append(ff)

        rarray = []
        for r in range(len(arrayf) - 1):
            if arrayf[r] in Farray:
                rarray.append(arrayf[r])

        if rarray != []:
            rmin = np.amin(rarray)

            Index = Farray.index(rmin)

            Aindex = SerieAcum[-Index - 1:]

            Ais = np.sum(Aindex)

            R1 = Res - Ais
            for a in range(len(Aindex)):
                Array.append(Aindex[a])

            if R1 > 0:
                if R1 in SerieAcum:
                    Array.append(int(R1))

                elif R1 < np.amin(SerieAcum):
                    R.append(int(R1))
                else:
                    for r in range(len(SerieAcum)):
                        T = R1 - SerieAcum[len(SerieAcum) - 1 - r]
                        if T > 0:
                            Array.append(SerieAcum[len(SerieAcum) - 1 - r])
                            R.append(int(T))
                            break

            '''--si el residuo "Res" esta cerca de el DivAcum que da menor residuo R1'''
        else:
            ffloat = np.amin(Farray)
            Index = Farray.index(ffloat)
            Aindex = SerieAcum[-Index - 1:]
            Ais = np.sum(Aindex)
            R1 = Res - Ais

            for a in range(len(Aindex)):
                Array.append(Aindex[a])

            if R1 > 0:
                if R1 in SerieAcum:
                    Array.append(int(R1))

                elif R1 < np.amin(SerieAcum):
                    R.append(int(R1))
                else:
                    for r in range(len(SerieAcum)):
                        T = R1 - SerieAcum[len(SerieAcum) - 1 - r]
                        if T > 0:
                            Array.append(SerieAcum[len(SerieAcum) - 1 - r])
                            R.append(int(T))
                            break


def PlotT2I(BD_ws, hk, G, Caudal, Capa, D, folderpath):
    # Pegar os dados de uma tabela e procurar o arquivo em um lugar certo e fazer umas interações
    Table = 'G{}Q{}KI'.format(G, Caudal)
    Id = 'K{}I'.format(hk)
    Record = readSingleRowTG(BD_ws, Table, Id)
    h = convert_array(Record[15])
    hmin = np.ma.round(h[Capa - 1].min(), decimals=1)
    hmax = np.ma.round(h[Capa - 1].max(), decimals=1)
    Fitcolor = (hmax - hmin) * 0.8 + hmin
    # --------------------------------------------------
    # MyFiles = Path(folderpath/'Documents/SaveByMe').mkdir(parents=True, exist_ok=True)
    MyFiles = os.path.join(folderpath, 'Documents/SaveByMe')
    # --------------------------------------------------
    Xt = np.array(list(it.accumulate(D)))
    x = Xt[:]
    y = x
    X, Y = np.meshgrid(x, y)
    Z = np.ma.round(h[Capa - 1], decimals=3)
    # --------------------------------------------------
    mg = StructuredGrid(delc=D, delr=D)

    def plot_lines(lines):
        for ln in lines:
            plt.plot([ln[0][0], ln[1][0]], [ln[0][1], ln[1][1]], alpha=0.15, color='k')

    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))  # Aquiw é onde começa a graficar
    ax = fig.add_subplot(1, 1, 1, aspect='equal')
    plt.scatter(mg.xcellcenters.ravel(), mg.ycellcenters.ravel(), s=1, c='k', alpha=0.1)
    t = ax.set_title('Fig {}: Cell vertices Celd Layer {}; hmin={:6.1f}, hmax={:6.1f}'.format(1, Capa, hmin, hmax),
                     loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig3 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # print(image_base64)

    # plt.savefig(MyFiles + '/f1.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, aspect='equal')  # DAQUI PRA FRENTE SAO TODAS AS FIGURAS
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    cint = .1
    cint2 = .001
    levels = np.arange(np.floor(hmin), np.ceil(hmax) + cint, cint)
    levels2 = np.arange(np.floor(Fitcolor), np.ceil(hmax) + cint2, cint2)
    c = plt.contour(x, y, Z, levels=levels, linewidths=2, colors='white')
    plt.clabel(c, inline=True, colors='white', fontsize=12, fmt='%2.1f')
    contour_filled = plt.contourf(x, y, Z, levels2, alpha=1, vmin=Fitcolor, vmax=hmax, cmap='jet')
    plt.colorbar(contour_filled)
    plot_lines(mg.grid_lines)
    line = np.array([(0, np.sum(D) / 2), (np.sum(D), np.sum(D) / 2)])
    plt.plot(line[:, 0], line[:, 1], 'b--', linewidth=3);
    t = ax.set_title('Fig {}: Layer {}; hmin={:6.1f}, hmax={:6.1f}'.format(2, Capa, hmin, hmax), loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig4 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f2.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    dhdx, dhdy = np.gradient(Z)  # dh/dx, dh/dy
    ax = fig.gca()
    ax.quiver(x, y, dhdx, dhdy, color='g', angles='xy', scale_units='xy')
    c = plt.contour(x, y, Z, levels=levels, linewidths=2, colors='k')
    plt.clabel(c, inline=True, colors='k', fontsize=12, fmt='%2.1f')
    plt.axis('equal')
    t = ax.set_title('Fig {}: vector Layer {}; hmin={:6.2f}, hmax={:6.2f}'.format(3, Capa, hmin, hmax), loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig5 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f3.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')
    ax.contour3D(x, y, Z, 50, cmap='binary')
    ax.view_init(60, 35)
    t = ax.set_title('Fig {}: 3d contour Layer {}; hmin={:6.2f}, hmax={:6.2f}'.format(4, Capa, hmin, hmax), loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig6 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f4.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')
    cset = ax.contour(x, y, Z, extend3d=True, cmap=cm.coolwarm)
    t = ax.set_title('Fig {}: 3d Cilindric contour Layer {}; hmin={:6.2f}, hmax={:6.2f}'.format(5, Capa, hmin, hmax),
                     loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig7 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f5.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z)
    ax.view_init(45, 60)
    t = ax.set_title('Fig {}: 3d Mesh Layer {}; hmin={:6.2f}, hmax={:6.2f}'.format(6, Capa, hmin, hmax), loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig8 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f6.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')
    ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    t = ax.set_title('Fig {}: 3d Grid Layer {}; hmin={:6.2f}, hmax={:6.2f}'.format(7, Capa, hmin, hmax), loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig9 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f7.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')
    mycmap = plt.get_cmap('gist_earth')
    surf = ax.plot_surface(X, Y, Z, cmap=mycmap)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    t = ax.set_title('Fig {}: 3d classification Layer {}; hmin={:6.2f}, hmax={:6.2f}'.format(8, Capa, hmin, hmax),
                     loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig10 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f8.png', format='png')
    # --------------------------------------------------
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.8, cmap=cm.ocean)
    cset = ax.contourf(X, Y, Z, zdir='z', offset=np.min(Z), cmap=cm.ocean)
    cset = ax.contourf(X, Y, Z, zdir='x', offset=-1, cmap=cm.ocean)
    cset = ax.contourf(X, Y, Z, zdir='y', offset=-1, cmap=cm.ocean)
    ax.view_init(30, 30)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    t = ax.set_title('Fig {}: 3d projection Layer {}; hmin={:6.2f}, hmax={:6.2f}'.format(9, Capa, hmin, hmax),
                     loc='left')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig11 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/f9.png', format='png')
    buf.close()
    return fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11


def PlotT3(BD_ws, hk, G, Caudal, ArrayEsp, Capa, C, F, P, ExagVert, Xmin, Xmax, topref, DeltaPlot):
    fig = plt.figure(figsize=(15, 15))
    # Criar outra aba para mostrar daqui pra frente
    Table = 'G{}Q{}KI'.format(G, Caudal)
    Id = 'K{}I'.format(hk)
    RecordD = readSingleRowTG(BD_ws, Table, Id)
    xd = convert_array(RecordD[2])
    Xt = np.array(list(it.accumulate(xd)))
    x = Xt[:]
    z = np.linspace(topref - 0.5, topref - P + 0.5, P)

    Table = 'resp3G{}Q{}KIP'.format(G, Caudal)
    Id = 'K{}C{}F{}P{}'.format(hk, C, F, P)
    RecordH = readSingleRowTG(BD_ws, Table, Id)
    h = convert_array(RecordH[5])
    H = np.where(h < 0, 0, h)
    kh1 = H[C + F - 1] != 0
    kh2 = H[C + F - 1]
    Kh3 = kh2[kh1]
    hmin = np.ma.round(np.amin(Kh3), decimals=3)
    HminC1 = H != 0
    HminC2 = H[HminC1]
    hminC3 = np.ma.round(np.amin(HminC2), decimals=3)
    hmax = np.ma.round(H[Capa - 1].max(), decimals=1)
    print(hmin, hminC3, hmax, h.shape, x.shape, z.shape)

    Long_p = int(np.sum(x))

    levels = np.arange(hminC3, hmax + DeltaPlot, DeltaPlot)
    c = plt.contour(x, z, h, levels=levels, colors='blue', linewidths=1.0)
    plt.clabel(c, fmt='%2.1f')
    plt.axis([Xmin, Xmax, topref - P, topref])
    plt.plot(x, h[Capa - 1], 'r--', linewidth=2)
    ax = plt.gca()
    ax.set_aspect(ExagVert)

    # grid lines
    for a in x:
        plt.plot([a, a], [z[0], z[-1]], color='black', alpha=.2, linestyle='-')
    for b in z:
        plt.plot([x[0], x[-1]], [b, b], color='black', alpha=.2, linestyle='-')

    # os.chdir('Documents/')
    # directorio_actual = os.getcwd()
    # carpeta = Path(directorio_actual)
    # MyFiles = Path(carpeta/'Documents/SaveByMe').mkdir(parents=True, exist_ok=True)
    # MyFiles = os.path.join(carpeta/'Documents/SaveByMe')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    fig10 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    # plt.savefig(MyFiles + '/Plot3.png', format='png')
    buf.close()
    # teste
    return fig10


def get_water_table(heads, per_idx=None):
    """Get a 2D array representing the water table
    elevation for each stress period in heads array.

    Parameters
    ----------
    heads : 3 or 4-D np.ndarray
        Heads array.
    nodata : real
        HDRY value indicating dry cells.
    per_idx : int or sequence of ints
        stress periods to return. If None,
        returns all stress periods (default).
    Returns
    -------
    wt : 2 or 3-D np.ndarray of water table elevations
        for each stress period.
    """
    heads = np.array(heads, ndmin=4)
    nper, nlay, nrow, ncol = heads.shape
    if per_idx is None:
        per_idx = list(range(nper))
    elif np.isscalar(per_idx):
        per_idx = [per_idx]
    wt = []
    for per in per_idx:
        wt_per = []
        for i in range(nrow):
            for j in range(ncol):
                for k in range(nlay):
                    if heads[per, k, i, j] >= 0:
                        wt_per.append(heads[per, k, i, j])
                        break
                    elif k == nlay - 1:
                        wt_per.append(0)
        assert len(wt_per) == nrow * ncol
        wt.append(np.reshape(wt_per, (nrow, ncol)))
    return np.squeeze(wt)


def get_gradients(heads, topref, nodata, per_idx=None):
    """Calculates the hydraulic gradients from the heads
    array for each stress period.
    Parameters
    ----------
    heads : 3 or 4-D np.ndarray
        Heads array.
    m : flopy.modflow.Modflow object
        Must have a flopy.modflow.ModflowDis object attached.
    nodata : real
        HDRY value indicating dry cells.
    per_idx : int or sequence of ints
        stress periods to return. If None,
        returns all stress periods (default).
    Returns
    -------
    grad : 3 or 4-D np.ndarray
        Array of hydraulic gradients
    """
    heads = np.array(heads, ndmin=4)
    nper, nlay, nrow, ncol = heads.shape
    if per_idx is None:
        per_idx = list(range(nper))
    elif np.isscalar(per_idx):
        per_idx = [per_idx]

    heads[heads == nodata] = np.nan

    grad = []
    for per in per_idx:
        hds = heads[per]
        a, b, c = hds.shape
        z = np.linspace(topref - 0.5, topref - a + 0.5, a)
        z1 = np.ones((b, c), dtype=np.int32)
        zcnt_per = np.array([i * z1 for i in z])
        unsat = zcnt_per > hds
        zcnt_per[np.isnan(hds)] = np.nan
        zcnt_per[unsat] = hds[unsat]

        dz = np.diff(zcnt_per, axis=0)
        dh = np.diff(hds, axis=0)
        grad.append(dh / dz)
    return np.squeeze(grad), unsat, hds, zcnt_per, dz, dh


def get_saturated_thickness(heads, topref, per_idx=None):
    """Calculates the saturated thickness for each cell from the heads
    array for each stress period.
    Parameters
    ----------
    heads : 3 or 4-D np.ndarray
        Heads array.
    m : flopy.modflow.Modflow object
        Must have a flopy.modflow.ModflowDis object attached.
    nodata : real
        HDRY value indicating dry cells.
    per_idx : int or sequence of ints
        stress periods to return. If None,
        returns all stress periods (default).
    Returns
    -------
    sat_thickness : 3 or 4-D np.ndarray
        Array of saturated thickness
    """
    heads = np.array(heads, ndmin=4)

    p, a, b, c = heads.shape
    b1 = np.linspace(topref - 5, topref - a * 5, a)
    b2 = np.ones((b, c), dtype=np.int32)
    botm = np.array([i * b2 for i in b1])
    t1 = np.ones(a)
    thickness = np.array([i * b2 for i in t1])

    nper, nlay, nrow, ncol = heads.shape
    if per_idx is None:
        per_idx = list(range(nper))
    elif np.isscalar(per_idx):
        per_idx = [per_idx]

    heads[heads <= 0] = np.nan
    sat_thickness = []
    for per in per_idx:
        hds = heads[per]
        perthickness = hds - botm
        # print(perthickness)
        conf = perthickness > thickness

        perthickness[conf] = thickness[conf]
        # print(perthickness)
        sat_thickness.append(perthickness)

    return np.squeeze(sat_thickness)
