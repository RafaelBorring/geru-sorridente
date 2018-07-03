from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core import forms
from calendar import LocaleHTMLCalendar
from django.utils.safestring import mark_safe
from datetime import datetime


def index(request):
    return render(request, 'core/index.html')


def cadastro(request):
    if request.method == "POST":
        form = forms.CadastroForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('auth.login')
    else:
        form = forms.CadastroForm
    return render(
        request, 'core/cadastro.html', {'form': form})


@login_required(login_url='/login')
def marcacao(request):
    if request.method == "POST":
        form = forms.MarcacaoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('auth.login')
    else:
        form = forms.MarcacaoForm
    return render(
        request, 'core/marcacao.html', {'form': form})


class Calendario(LocaleHTMLCalendar):

    def __init__(self):
        super(Calendario, self).__init__(6, 'pt_BR.UTF-8')


def calendario(request):

    hoje = datetime.now()
    c = Calendario().formatmonth(hoje.year, hoje.month)

    return render(
        request, 'core/calendario.html', {'calendario': mark_safe(c)})
