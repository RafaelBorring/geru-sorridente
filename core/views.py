from calendar import LocaleHTMLCalendar, different_locale, month_name
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

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
def marcacao(request, ano, mes, dia):
    with different_locale('pt_BR.UTF-8'):
        data = '{:02d} de {} de {}'.format(dia, month_name[mes], ano)
    if request.method == "POST":
        form = forms.MarcacaoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.data = '{}-{}-{}'.format(ano, mes, dia)
            post.save()
            return render(request, 'core/realizada.html', {'data': data})
    else:
        form = forms.MarcacaoForm
    return render(
        request, 'core/marcacao.html', {'form': form, 'data': data})


class Calendario(LocaleHTMLCalendar):
    def __init__(self):
        super(Calendario, self).__init__(6, 'pt_BR.UTF-8')

    def formatmonth(self, ano, mes):
        self.ano = ano
        self.mes = mes
        return super(Calendario, self).formatmonth(ano, mes)

    def formatday(self, dia, semana):
        if dia == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            return '<td class="{}"><a href="/marcacao/{}/{}/{}">{}</a></td>'\
                .format(self.cssclasses[semana], self.ano, self.mes, dia, dia)


def calendario(request):
    hoje = datetime.now()
    c = Calendario().formatmonth(hoje.year, hoje.month)

    return render(
        request, 'core/calendario.html', {'calendario': mark_safe(c)})
