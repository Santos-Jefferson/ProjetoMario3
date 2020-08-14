from django import forms


class PaginaInputForm(forms.Form):
    numceldasi = forms.IntegerField(label='Num Cel', initial=10)
    numlayi = forms.IntegerField(label='Num Lay', initial=10)
    topref = forms.IntegerField(label='Superfície do Solo', initial=100)
    botref = forms.IntegerField(label='Profundidade do Solo', initial=50)
    g = forms.IntegerField(label='G', initial=0)
    h1 = forms.IntegerField(label='H1', initial=100)
    hk = forms.IntegerField(label='HK', initial=1)
    # vk = forms.IntegerField(label='VK')
    caudal = forms.IntegerField(label='Caudal', initial=1)


class Plot3InputForm(forms.Form):
    hk = forms.IntegerField(label='HK', initial=1)
    g = forms.IntegerField(label='G', initial=0)
    caudal = forms.IntegerField(label='Caudal', initial=1)
    topref = forms.IntegerField(label='Superfície do Solo', initial=100)

    capa1 = forms.IntegerField(label='Capa1', initial=1)
    c1 = forms.IntegerField(label='C1', initial=9)
    f1 = forms.IntegerField(label='F1', initial=5)
    p1 = forms.IntegerField(label='P1', initial=50)
    exagvert1 = forms.IntegerField(label='ExagVert1', initial=100)
    xmin1 = forms.IntegerField(label='Xmin1', initial=1)
    xmax1 = forms.IntegerField(label='Xmax1', initial=11161)
    ymin1 = forms.IntegerField(label='Ymin1', initial=80)
    deltaplot1 = forms.FloatField(label='DeltaPlot1', initial=0.1)

    capa2 = forms.IntegerField(label='Capa2', initial=1)
    c2 = forms.IntegerField(label='C2', initial=9)
    f2 = forms.IntegerField(label='F2', initial=5)
    p2 = forms.IntegerField(label='P2', initial=28)
    exagvert2 = forms.IntegerField(label='ExagVert2', initial=1)
    xmin2 = forms.IntegerField(label='Xmin2', initial=5450)
    xmax2 = forms.IntegerField(label='Xmax2', initial=5700)
    ymin2 = forms.IntegerField(label='Ymin2', initial=80)
    deltaplot2 = forms.FloatField(label='DeltaPlot2', initial=0.1)

    capa3 = forms.IntegerField(label='Capa3', initial=1)
    c3 = forms.IntegerField(label='C3', initial=9)
    f3 = forms.IntegerField(label='F3', initial=5)
    p3 = forms.IntegerField(label='P3', initial=17)
    exagvert3 = forms.IntegerField(label='ExagVert3', initial=10)
    xmin3 = forms.IntegerField(label='Xmin3', initial=5100)
    xmax3 = forms.IntegerField(label='Xmax3', initial=6100)
    ymin3 = forms.IntegerField(label='Ymin3', initial=80)
    deltaplot3 = forms.FloatField(label='DeltaPlot3', initial=0.1)

    capa4 = forms.IntegerField(label='Capa4', initial=1)
    c4 = forms.IntegerField(label='C4', initial=9)
    f4 = forms.IntegerField(label='F4', initial=5)
    p4 = forms.IntegerField(label='P4', initial=15)