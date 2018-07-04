from django import forms
from django.contrib.auth.forms import UserCreationForm

from core import models


class CadastroForm(UserCreationForm):
    class Meta:
        model = models.Cadastro
        fields = ['cns', 'nome', 'nascimento', 'endereco', 'telefone', 'acs']


class MarcacaoForm(forms.ModelForm):
    class Meta:
        model = models.Marcacao
        fields = ['motivo', 'protese']
