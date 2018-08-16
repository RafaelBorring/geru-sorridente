from calendar import LocaleHTMLCalendar, different_locale, month_name
from datetime import date
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from core import forms, models


def index(request):
    if request.method == "POST":
        form = forms.UsuarioForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('auth.login')
    else:
        form = forms.UsuarioForm
    return render(request, 'core/index.html', {'form': form})


@login_required(login_url='auth.login')
def marcacao(request, ano, mes, dia):
    with different_locale('pt_BR.UTF-8'):
        dia_marcacao = date(ano, mes, dia)
        data = '{:02d} de {} de {}'.format(dia, month_name[mes], ano)
    if dia_marcacao <= date.today() or dia_marcacao.weekday() in [5, 6]:
        return redirect('core.index')
    elif request.method == "POST":
        form = forms.MarcacaoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.data = dia_marcacao.strftime('%Y-%m-%d')
            listed = models.Marcacao.objects.filter(
                user=post.user
            ).order_by('data').reverse()
            if listed:
                last_date = listed[0].data.toordinal()
            else:
                last_date = date.today().toordinal() - 15
            if date.today().toordinal() - last_date <= 0:
                return render(request, 'core/marcacao.html', {
                    'form': form, 'data': data,
                    'message': '''
                    Já existe uma consulta agendada no dia {}
                    '''.format(
                        date.fromordinal(last_date).strftime('%d/%m/%Y')
                    )})
            elif dia_marcacao.toordinal() - last_date <= 15:
                return render(request, 'core/marcacao.html', {
                    'form': form, 'data': data,
                    'message': '''
                    Última consulta realizada em {}\n
                    A próxima só pode ser realizada a partir do dia {}
                    '''.format(
                        date.fromordinal(last_date).strftime('%d/%m/%Y'),
                        date.fromordinal(last_date + 16).strftime('%d/%m/%Y')
                    )})
            elif post.user.locked:
                return render(request, 'core/marcacao.html', {
                    'form': form, 'data': data,
                    'message': '''
                    Usuário bloqueado por não comparecer a uma consulta\n
                    Procure por {} para dar uma justificativa
                    '''.format(
                        post.user.acs.nome
                    )})
            post.save()
            return render(request, 'core/realizada.html', {
                'id': post.id,
                'data': data
                })
    else:
        form = forms.MarcacaoForm
    return render(request, 'core/marcacao.html', {'form': form, 'data': data})


class Calendario(LocaleHTMLCalendar):
    def __init__(self, user, hoje):
        super(Calendario, self).__init__(6, 'pt_BR.UTF-8')
        self.equipe = user.acs.equipe
        self.micro = user.acs
        self.hoje = hoje

    def formatmonth(self, ano, mes):
        self.ano = ano
        self.mes = mes
        return super(Calendario, self).formatmonth(ano, mes)

    def formatday(self, dia, semana):
        if dia == 0 or semana in [5, 6] or dia <= self.hoje:
            return '<td class="noday">&nbsp;</td>'
        else:
            vagas = 5 - models.Marcacao.objects.filter(
                data='{}-{}-{}'.format(self.ano, self.mes, dia),
                user__acs__equipe=self.equipe,
                user__acs=self.micro).count()
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
                    .format(
                    self.cssclasses[semana], self.ano, self.mes, dia, dia,
                    vagas
                )
            else:
                return '<td class="{}">\
                <a class="btn btn-warning"\
                href="/marcacao/{}/{}/{}">{:02d}</a>\
                <h5>{} Vaga</h5>\
                </td>'\
                    .format(
                    self.cssclasses[semana], self.ano, self.mes, dia, dia,
                    vagas
                )


@login_required(login_url='auth.login')
def calendario(request):
    hoje = date.today()
    user = request.user
    c = Calendario(user, hoje.day).formatmonth(hoje.year, hoje.month)
    return render(
        request, 'core/calendario.html', {
            'calendario': mark_safe(c), 'equipe': user.acs.equipe
        }
    )


@login_required(login_url='auth.login')
def consultas(request):
    user = request.user
    listed = models.Marcacao.objects.filter(user=user).order_by('-data')
    return render(
        request, 'core/consultas.html', {
            'consultas': listed
        }
    )


@login_required(login_url='auth.login')
def requisicao(request, id):
    user = request.user
    req = models.Marcacao.objects.get(id=id)
    margin = 2*cm
    x, y = A4
    response = HttpResponse(content_type='application/pdf')
    tmp_pdf = BytesIO()
    pdf = Canvas(tmp_pdf, pagesize=A4)
    pdf.setFont('Times-Bold', 14)
    pdf.drawString(
        margin, y-margin, 'Secretaria Municipal de Saúde de Tomar do Geru'
    )
    pdf.drawString(
        x-margin-4.5*cm, y-margin,
        'Emissão: {}'.format(date.today().strftime('%d/%m/%Y'))
    )
    pdf.drawString(
        margin, y-margin-cm, 'Requisição de Consulta Odontológica'
    )
    pdf.line(margin, y-margin-1.3*cm, x-margin, y-margin-1.3*cm)
    pdf.drawString(
        margin, y-margin-2*cm, 'Unidade:'
    )
    pdf.drawString(
        margin, y-margin-3*cm, 'Equipe:'
    )
    pdf.drawString(
        margin, y-margin-4*cm, 'Data:'
    )
    pdf.line(margin, y-margin-4.3*cm, x-margin, y-margin-4.3*cm)
    pdf.drawString(
        margin, y-margin-5*cm, 'CNS:'
    )
    pdf.drawString(
        margin, y-margin-6*cm, 'Nome:'
    )
    pdf.drawString(
        margin, y-margin-7*cm, 'Logradouro:'
    )
    pdf.setFont('Times-Roman', 14)
    pdf.drawString(
        margin+3*cm, y-margin-2*cm, '{}'.format(req.user.acs.equipe.unidade)
    )
    pdf.drawString(
        margin+3*cm, y-margin-3*cm, '{}'.format(req.user.acs.equipe)
    )
    pdf.drawString(
        margin+3*cm, y-margin-4*cm, '{}'.format(req.data.strftime('%d/%m/%Y'))
    )
    pdf.drawString(
        margin+3*cm, y-margin-5*cm, user.cns
    )
    pdf.drawString(
        margin+3*cm, y-margin-6*cm, user.nome
    )
    pdf.drawString(
        margin+3*cm, y-margin-7*cm, user.endereco
    )
    pdf.showPage()
    pdf.save()
    response.write(tmp_pdf.getvalue())
    tmp_pdf.close()
    return response
