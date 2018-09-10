from calendar import TextCalendar, day_name, different_locale, month_name
from re import match

from django import forms
from django.contrib.auth.forms import UserCreationForm

from core import models


class UsuarioForm(UserCreationForm):
    class Meta:
        model = models.Usuario
        fields = ['cns', 'nome', 'nascimento', 'endereco', 'telefone', 'acs']

    def clean_cns(self):
        self.cns = self.cleaned_data['cns']
        soma = 0
        contador = 15
        for cns in self.cns:
            if cns not in [None, ' ']:
                soma += int(cns) * contador
                contador -= 1
        t = soma % 11 == 0
        if not match(r'^[7-9]\d{2}\s\d{4}\s\d{4}\s\d{4}$', self.cns) and t:
            raise forms.ValidationError('Número de cartão inválido!')
        elif match(r'^[1-2]\d{2}\s\d{4}\s\d{4}\s00[0-1]\d$', self.cns) and t:
            raise forms.ValidationError('Seu cartão está desatualizado!')
        return self.cns


class MarcacaoForm(forms.ModelForm):
    class Meta:
        model = models.Marcacao
        fields = ['motivo', 'protese']
        widgets = {
            'motivo': forms.RadioSelect,
            'protese': forms.RadioSelect
        }


class AgendaForm(forms.ModelForm):
    class Meta:
        model = models.Agenda
        fields = ['dia', 'vaga', 'tempo']

    def __init__(self, *args, **kwargs):
        self.ano = kwargs.pop('ano')
        self.mes = kwargs.pop('mes')
        super(AgendaForm, self).__init__(*args, **kwargs)
        vaga_dia = []
        with different_locale('pt_BR.UTF-8'):
            for semanas in TextCalendar().monthdatescalendar(
                self.ano, self.mes
            ):
                for dias in semanas:
                    if dias.month == self.mes and dias.weekday() not in [5, 6]:
                        vaga_dia.append((
                            dias.day,
                            '{:02d} - {}'.format(
                                dias.day, day_name[dias.weekday()].title()
                            )
                        ))
        self.fields['dia'].widget = forms.CheckboxSelectMultiple()
        self.fields['dia'].widget.choices = vaga_dia

    def clean(self):
        if models.Agenda.objects.filter(ano=self.ano, mes=self.mes):
            raise forms.ValidationError('Já existe agenda nesse mês!')
        return self.cleaned_data
