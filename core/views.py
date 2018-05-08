from django.shortcuts import render
from core import forms


def index(request):
    return render(request, 'core/index.html')


def cadastro(request):
    if request.method == "POST":
        form = forms.CadastroForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = forms.CadastroForm
    return render(
        request, 'core/cadastro.html', {'form': forms.CadastroForm()})
