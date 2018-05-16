from django.shortcuts import render, redirect
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
