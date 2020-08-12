from django import forms


class PaginaInputForm(forms.Form):
    numceldasi = forms.IntegerField(label='Num Cel')
    numlayi = forms.IntegerField(label='Num Lay')
    topref = forms.IntegerField(label='Superfície do Solo')
    botref = forms.IntegerField(label='Profundidade do Solo')
    g = forms.IntegerField(label='G')
    h1 = forms.IntegerField(label='H1')
    hk = forms.IntegerField(label='HK')
    # vk = forms.IntegerField(label='VK')
    caudal = forms.IntegerField(label='Caudal')


class Plot3InputForm(forms.Form):
    hk = forms.IntegerField(label='HK')
    g = forms.IntegerField(label='G')
    caudal = forms.IntegerField(label='Caudal')
    topref = forms.IntegerField(label='Superfície do Solo')
    #test


    capa1 = forms.IntegerField(label='Capa1')
    c1 = forms.IntegerField(label='C1')
    f1 = forms.IntegerField(label='F1')
    p1 = forms.IntegerField(label='P1')
    exagvert1 = forms.IntegerField(label='ExagVert1')
    xmin1 = forms.IntegerField(label='Xmin1')
    xmax1 = forms.IntegerField(label='Xmax1')
    ymin1 = forms.IntegerField(label='Ymin1')
    deltaplot1 = forms.FloatField(label='DeltaPlot1')

    capa2 = forms.IntegerField(label='Capa2')
    c2 = forms.IntegerField(label='C2')
    f2 = forms.IntegerField(label='F2')
    p2 = forms.IntegerField(label='P2')
    exagvert2 = forms.IntegerField(label='ExagVert2')
    xmin2 = forms.IntegerField(label='Xmin2')
    xmax2 = forms.IntegerField(label='Xmax2')
    ymin2 = forms.IntegerField(label='Ymin2')
    deltaplot2 = forms.FloatField(label='DeltaPlot2')

    capa3 = forms.IntegerField(label='Capa3')
    c3 = forms.IntegerField(label='C3')
    f3 = forms.IntegerField(label='F3')
    p3 = forms.IntegerField(label='P3')
    exagvert3 = forms.IntegerField(label='ExagVert3')
    xmin3 = forms.IntegerField(label='Xmin3')
    xmax3 = forms.IntegerField(label='Xmax3')
    ymin3 = forms.IntegerField(label='Ymin3')
    deltaplot3 = forms.FloatField(label='DeltaPlot3')

    capa4 = forms.IntegerField(label='Capa4')
    c4 = forms.IntegerField(label='C4')
    f4 = forms.IntegerField(label='F4')
    p4 = forms.IntegerField(label='P4')