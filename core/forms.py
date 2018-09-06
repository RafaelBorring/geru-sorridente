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
        fields = ['mes', 'ano', 'dia', 'vaga', 'tempo']

    with different_locale('pt_BR.UTF-8'):
        MES_DO_ANO = tuple(
            (list(month_name).index(x), x.title()) for x in month_name
        )
    mes = forms.ChoiceField(choices=MES_DO_ANO, label='Mês de Referência')
    dia = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Dias da Semana'
    )

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        vaga_dia = []
        with different_locale('pt_BR.UTF-8'):
            for semanas in TextCalendar().monthdatescalendar(2018, 9):
                for dias in semanas:
                    if dias.month == 9:
                        vaga_dia.append((
                            dias.day,
                            '{:02d} - {}'.format(
                                dias.day, day_name[dias.weekday()].title()
                            )
                        ))
        self.fields['dia'].widget.choices = vaga_dia

    def clean(self):
        mes = self.cleaned_data['mes']
        ano = self.cleaned_data['ano']
        if models.Agenda.objects.filter(ano=ano, mes=mes):
            raise forms.ValidationError('Já existe agenda nesse mês!')
        return self.cleaned_data
