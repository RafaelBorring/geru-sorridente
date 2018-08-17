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
        if match(r'^[7-9]\d{2}\s\d{4}\s\d{4}\s\d{4}$', self.cns) and t:
            return self.cns
        elif match(r'^[1-2]\d{2}\s\d{4}\s\d{4}\s00[0-1]\d$', self.cns) and t:
            raise forms.ValidationError('Seu cartão está desatualizado!')
        else:
            raise forms.ValidationError('Número de cartão inválido!')


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
        widgets = {
            'dia': forms.SelectMultiple,
        }
