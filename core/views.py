from calendar import LocaleHTMLCalendar, different_locale, month_name
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from core import forms, models


def index(request):
    if request.method == "POST":
        form = forms.CadastroForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('auth.login')
    else:
        form = forms.CadastroForm
    return render(request, 'core/index.html', {'form': form})


@login_required(login_url='auth.login')
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
    def __init__(self, user, hoje):
        super(Calendario, self).__init__(6, 'pt_BR.UTF-8')
        self.equipe = user.acs.equipe
        self.hoje = hoje

    def formatmonth(self, ano, mes):
        self.ano = ano
        self.mes = mes
        return super(Calendario, self).formatmonth(ano, mes)

    def formatday(self, dia, semana):
        if dia == 0 or dia <= self.hoje:
            return '<td class="noday">&nbsp;</td>'
        else:
            vagas = 10 - models.Marcacao.objects.filter(
                data='{}-{}-{}'.format(self.ano, self.mes, dia),
                user__acs__equipe=self.equipe).count()
            if vagas == 0:
                return '<td class="{}">\
                <a class="btn btn-danger" href="#">{:02d}</a>\
                <h5>{} Vagas</h5>\
                </td>'\
                    .format(self.cssclasses[semana], dia, vagas)
            if vagas > 1:
                return '<td class="{}">\
                <a class="btn btn-success"\
                href="/marcacao/{}/{}/{}">{:02d}</a>\
                <h5>{} Vagas</h5>\
                </td>'\
                    .format(self.cssclasses[semana], self.ano, self.mes, dia,
                            dia, vagas)
            else:
                return '<td class="{}">\
                <a class="btn btn-warning"\
                href="/marcacao/{}/{}/{}">{:02d}</a>\
                <h5>{} Vaga</h5>\
                </td>'\
                    .format(self.cssclasses[semana], self.ano, self.mes, dia,
                            dia, vagas)


def calendario(request):
    hoje = datetime.today()
    user = request.user
    c = Calendario(user, hoje.day).formatmonth(hoje.year, hoje.month)

    return render(
        request, 'core/calendario.html', {'calendario': mark_safe(c),
                                          'equipe': user.acs.equipe})
