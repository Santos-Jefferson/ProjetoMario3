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
