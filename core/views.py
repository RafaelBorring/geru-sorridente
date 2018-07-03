from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core import forms


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
