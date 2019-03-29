"""
Views controller.
"""
from calendar import LocaleHTMLCalendar, different_locale, month_name
from datetime import date
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from core import forms, models


def index(request):
    """Home Page."""
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
    """Marcação de consultas."""
    user = request.user
    with different_locale('pt_BR.UTF-8'):
        dia_marcacao = date(ano, mes, dia)
        data = '{:02d} de {} de {}'.format(dia, month_name[mes], ano)
    try:
        dias_marc1 = models.Agenda.objects.get(ano=ano, mes=mes, equipe=1)
    except models.Agenda.DoesNotExist:
        dias_marc1 = None
    try:
        dias_marc2 = models.Agenda.objects.get(ano=ano, mes=mes, equipe=2)
    except models.Agenda.DoesNotExist:
        dias_marc2 = None
    try:
        dias_marc4 = models.Agenda.objects.get(ano=ano, mes=mes, equipe=4)
    except models.Agenda.DoesNotExist:
        dias_marc4 = None
    if dias_marc1:
        dias1 = [int(i) for i in dias_marc1.dia.split("'") if i.isdigit()]
    if dias_marc2:
        dias2 = [int(i) for i in dias_marc2.dia.split("'") if i.isdigit()]
    if dias_marc4:
        dias4 = [int(i) for i in dias_marc4.dia.split("'") if i.isdigit()]
    if dia_marcacao <= date.today() or (not dias_marc1 and not dias_marc2 and not dias_marc4) or\
            (dia not in dias1 and dia not in dias2 and dia not in dias4):
        return redirect('core.index')
    elif request.method == "POST":
        form = forms.MarcacaoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.data = dia_marcacao.strftime('%Y-%m-%d')
            listed = models.Marcacao.objects.filter(user=post.user).order_by('data').reverse()
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
            elif post.user.is_locked:
                return render(request, 'core/marcacao.html', {
                    'form': form, 'data': data,
                    'message': '''
                    Usuário bloqueado por não comparecer a uma consulta\n
                    Procure por {} (ACS) para dar uma justificativa
                    '''.format(post.user.acs.nome)})
            post.save()
            return render(request, 'core/realizada.html', {'get_id': post.id, 'data': data})
    else:
        form = forms.MarcacaoForm
    return render(request, 'core/marcacao.html', {'form': form, 'data': data})


class Calendario(LocaleHTMLCalendar):
    """Calendário HTML."""

    def __init__(self, user, hoje):
        super(Calendario, self).__init__(6, 'pt_BR.UTF-8')
        self.tipo = user.tipo
        self.hoje = hoje
        if self.tipo == 1:
            self.equipe = user.equipe
        elif self.tipo == 3:
            self.equipe = user.acs.equipe
            self.micro = user.acs

    def formatmonth(self, ano, mes):
        """Formata o mês."""
        self.ano = ano
        self.mes = mes
        return super(Calendario, self).formatmonth(ano, mes)

    def formatday(self, dia, semana):
        """Formata o dia."""
        try:
            dias_marc1 = models.Agenda.objects.get(ano=self.ano, mes=self.mes, equipe=1)
        except models.Agenda.DoesNotExist:
            dias_marc1 = None
        try:
            dias_marc2 = models.Agenda.objects.get(ano=self.ano, mes=self.mes, equipe=2)
        except models.Agenda.DoesNotExist:
            dias_marc2 = None
        try:
            dias_marc4 = models.Agenda.objects.get(ano=self.ano, mes=self.mes, equipe=4)
        except models.Agenda.DoesNotExist:
            dias_marc4 = None
        if dias_marc1:
            dias1 = [int(i) for i in dias_marc1.dia.split("'") if i.isdigit()]
        else:
            dias1 = []
        if dias_marc2:
            dias2 = [int(i) for i in dias_marc2.dia.split("'") if i.isdigit()]
        else:
            dias2 = []
        if dias_marc4:
            dias4 = [int(i) for i in dias_marc4.dia.split("'") if i.isdigit()]
        else:
            dias4 = []
        if dia == 0 or (not dias_marc1 and not dias_marc2 and not dias_marc4) or\
                (dia not in dias1 and dia not in dias2 and dia not in dias4):
            return '<td class="noday">&nbsp;</td>'
        elif self.tipo == 1 and dia <= self.hoje:
            vagas = models.Marcacao.objects.filter(
                data='{}-{}-{}'.format(self.ano, self.mes, dia),
                user__acs__equipe=self.equipe
            ).count()
            return '''
                <td class="{}">
                    <a class="btn btn-warning" href="/bloquear/{}/{}/{}">
                        {:02d}
                    </a>
                    <h5>Total {}</h5>
                </td>
                '''.format(self.cssclasses[semana], self.ano, self.mes, dia, dia, vagas)
        elif self.tipo == 1:
            consulta_id = '{}{}{}{}'.format(self.equipe.area, self.ano, self.mes, dia)
            vagas = models.Marcacao.objects.filter(
                data='{}-{}-{}'.format(self.ano, self.mes, dia),
                user__acs__equipe=self.equipe, ativo=True
            ).count()
            return '''
            <td class="{}">
                <button type="button" class="btn btn-success"
                    data-toggle="modal" data-target="#{}">{:02d}</button>
                <h5>Total {}</h5>
            </td>
            <div class="modal fade" id="{}" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="{}">Lista</h5>
                            <button type="button" class="close"
                                data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <object type="application/pdf"
                                data="{}#zoom=page-width" width="100%"
                                height="100%">
                            </object>
                        </div>
                    </div>
                </div>
            </div>
            '''.format(
                self.cssclasses[semana], consulta_id, dia, vagas, consulta_id, consulta_id,
                reverse('core.lista', args=[self.ano, self.mes, dia])
            )
        elif dia <= self.hoje:
            return '<td class="noday">&nbsp;</td>'
        elif self.tipo == 3:
            if dias_marc1:
                total_vagas = models.Agenda.objects.get(ano=self.ano, mes=self.mes, equipe=1)
            if dias_marc2:
                total_vagas = models.Agenda.objects.get(ano=self.ano, mes=self.mes, equipe=2)
            if dias_marc4:
                total_vagas = models.Agenda.objects.get(ano=self.ano, mes=self.mes, equipe=4)
            vagas = total_vagas.vaga - models.Marcacao.objects.filter(
                data='{}-{}-{}'.format(self.ano, self.mes, dia), ativo=True
            ).count()
            if vagas == 0:
                return '''
                <td class="{}">
                    <a class="btn btn-danger" href="#">
                        {:02d}
                    </a>
                    <h5>{} Vagas</h5>
                </td>
                '''.format(self.cssclasses[semana], dia, vagas)
            elif vagas > 1:
                return '''
                <td class="{}">
                    <a class="btn btn-success" href="/marcacao/{}/{}/{}">
                        {:02d}
                    </a>
                    <h5>{} Vagas</h5>
                </td>
                '''.format(self.cssclasses[semana], self.ano, self.mes, dia, dia, vagas)
            return '''
            <td class="{}">
                <a class="btn btn-warning" href="/marcacao/{}/{}/{}">
                    {:02d}
                </a>
                <h5>{} Vaga</h5>
            </td>
            '''.format(self.cssclasses[semana], self.ano, self.mes, dia, dia, vagas)


@login_required(login_url='auth.login')
def calendario(request):
    """Calendário de vagas."""
    hoje = date.today()
    user = request.user
    call = Calendario(user, hoje.day).formatmonth(hoje.year, hoje.month)
    if user.tipo == 1:
        equipe = user.equipe
    elif user.tipo == 3:
        equipe = user.acs.equipe
    return render(
        request, 'core/calendario.html', {'calendario': mark_safe(call), 'equipe': equipe}
    )


@login_required(login_url='auth.login')
def consultas(request):
    """Lista consultas."""
    user = request.user
    listed = models.Marcacao.objects.filter(user=user).order_by('-data')
    return render(request, 'core/consultas.html', {'consultas': listed})


@login_required(login_url='auth.login')
def requisicao(request, get_id):
    """Impressão da requisição."""
    user = request.user
    req = models.Marcacao.objects.get(id=get_id)
    dia = req.data.strftime('%d')
    mes = req.data.strftime('%m')
    ano = req.data.strftime('%Y')
    agenda1 = models.Agenda.objects.get(mes=mes, ano=ano, equipe=1)
    agenda2 = models.Agenda.objects.get(mes=mes, ano=ano, equipe=2)
    agenda4 = models.Agenda.objects.get(mes=mes, ano=ano, equipe=4)
    if dia in agenda1.dia:
        agenda = agenda1
    if dia in agenda2.dia:
        agenda = agenda2
    if dia in agenda4.dia:
        agenda = agenda4
    margin = 2*cm
    x, y = A4
    response = HttpResponse(content_type='application/pdf')
    tmp_pdf = BytesIO()
    pdf = Canvas(tmp_pdf, pagesize=A4)
    pdf.setFont('Times-Bold', 14)
    pdf.drawString(margin, y-margin, 'Secretaria Municipal de Saúde de Tomar do Geru')
    pdf.drawString(
        x-margin-4.5*cm, y-margin, 'Emissão: {}'.format(date.today().strftime('%d/%m/%Y'))
    )
    pdf.drawString(margin, y-margin-cm, 'Requisição de Consulta Odontológica')
    pdf.line(margin, y-margin-1.3*cm, x-margin, y-margin-1.3*cm)
    pdf.drawString(margin, y-margin-2*cm, 'Unidade:')
    pdf.drawString(margin, y-margin-3*cm, 'Equipe:')
    pdf.drawString(margin, y-margin-4*cm, 'Data:')
    pdf.line(margin, y-margin-4.3*cm, x-margin, y-margin-4.3*cm)
    pdf.drawString(margin, y-margin-5*cm, 'CNS:')
    pdf.drawString(margin, y-margin-6*cm, 'Nome:')
    pdf.drawString(margin, y-margin-7*cm, 'Logradouro:')
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(margin+3*cm, y-margin-2*cm, '{}'.format(agenda.equipe.unidade))
    pdf.drawString(margin+3*cm, y-margin-3*cm, '{}'.format(agenda.equipe))
    pdf.drawString(margin+3*cm, y-margin-4*cm, '{}'.format(req.data.strftime('%d/%m/%Y')))
    pdf.drawString(margin+3*cm, y-margin-5*cm, user.cns)
    pdf.drawString(margin+3*cm, y-margin-6*cm, user.nome)
    pdf.drawString(margin+3*cm, y-margin-7*cm, user.endereco)
    pdf.showPage()
    pdf.save()
    response.write(tmp_pdf.getvalue())
    tmp_pdf.close()
    return response


@login_required(login_url='auth.login')
def lista(request, ano, mes, dia):
    """Lista de pacientes."""
    user = request.user
    listed = models.Marcacao.objects.filter(data='{}-{}-{}'.format(ano, mes, dia)).order_by('pk')
    margin = 2*cm
    x, y = A4
    response = HttpResponse(content_type='application/pdf')
    with different_locale('pt_BR.UTF-8'):
        filename = '{} - {:02d} de {} de {}'.format(user.equipe, dia, month_name[mes].title(), ano)
    response['Content-Disposition'] = 'filename="{}"'.format(filename)
    tmp_pdf = BytesIO()
    pdf = Canvas(tmp_pdf, pagesize=A4)
    pdf.setFont('Times-Bold', 14)
    pdf.drawString(margin, y-margin, '{}'.format(user.equipe))
    pdf.drawString(x-margin-cm, y-margin, '{:02d}/{:02d}/{}'.format(dia, mes, ano))
    top = y-cm
    pdf.drawString(margin, top-margin, 'CNS/CONTATO')
    pdf.drawString(margin+4.5*cm, top-margin, 'NOME')
    pdf.drawString(x-margin-5*cm, top-margin, 'MOTIVO')
    pdf.drawString(x-margin-cm, top-margin, 'PRÓTESE')
    pdf.setFont('Times-Roman', 10)
    for list_value in listed:
        top -= cm
        pdf.drawString(margin, top-margin+0.15*cm, '{}'.format(list_value.user.cns))
        pdf.drawString(margin, top-margin-0.15*cm, '{}'.format(list_value.user.telefone))
        pdf.drawString(margin+4.5*cm, top-margin, '{}'.format(list_value.user.nome))
        pdf.drawString(x-margin-5*cm, top-margin, '{}'.format(list_value.motivo))
        pdf.drawString(x-margin-cm, top-margin, '{}'.format(list_value.get_protese_display()))
        if not list_value.ativo:
            pdf.line(margin, top-margin+3, x-margin, top-margin+3)
    pdf.showPage()
    pdf.save()
    response.write(tmp_pdf.getvalue())
    tmp_pdf.close()
    if user.tipo == 1:
        return response
    return render(request, 'core/index.html')


@login_required(login_url='auth.login')
def agenda_mes(request):
    """Agenda do mês."""
    now = date.today()
    return render(request, 'core/agenda_mes.html', {'ano': now.year})


@login_required(login_url='auth.login')
def agenda_closed(request):
    """Agenda fechada."""
    user = request.user
    now = date.today()
    listed = models.Agenda.objects.filter(equipe=user.equipe, ano=now.year)
    data = serialize('json', listed)
    if user.tipo == 1:
        return HttpResponse(data, content_type='application/json')
    return render(request, 'core/index.html')


@login_required(login_url='auth.login')
def agenda(request, ano, mes):
    """Cria agenda."""
    with different_locale('pt_BR.UTF-8'):
        nome_mes = month_name[mes].title()
    user = request.user
    if user.tipo == 1:
        if request.method == "POST":
            form = forms.AgendaForm(request.POST, ano=ano, mes=mes, equipe=user.equipe)
            if form.is_valid():
                post = form.save(commit=False)
                post.ano = ano
                post.mes = mes
                post.equipe = user.equipe
                post.save()
                return render(request, 'core/criada.html')
        form = forms.AgendaForm(ano=ano, mes=mes, equipe=user.equipe)
        return render(request, 'core/agenda.html', {'form': form, 'ano': ano, 'mes': nome_mes})
    return render(request, 'core/index.html')


@login_required(login_url='auth.login')
def bloquear(request, ano, mes, dia):
    """Bloqueia usuário."""
    user = request.user
    data = '{}-{}-{}'.format(ano, mes, dia)
    lista = models.Marcacao.objects.filter(user__acs__equipe=user.equipe, data=data).order_by('pk')
    if request.method == "POST":
        for i in lista:
            if request.POST.get('{}'.format(i.user)) == 'on':
                usu_lock = models.Usuario.objects.get(pk=i.user.id)
                usu_lock.is_locked = True
                usu_lock.save()
        form = forms.BloquearForm(lista=lista)
        return redirect('core.calendario')
    form = forms.BloquearForm(lista=lista)
    if user.tipo == 1:
        return render(request, 'core/bloquear.html', {'form': form})
    return render(request, 'core/index.html')


@login_required(login_url='auth.login')
def desbloquear(request):
    """Desbloqueia usuário."""
    user = request.user
    lista = models.Usuario.objects.filter(acs=user, is_locked=True).order_by('nome')
    if request.method == "POST":
        for i in lista:
            if request.POST.get('{}'.format(i)) == 'on':
                usu_unlock = models.Usuario.objects.get(pk=i.id)
                usu_unlock.is_locked = False
                usu_unlock.save()
        form = forms.DesbloquearForm(lista=lista)
        return redirect('core.index')
    form = forms.DesbloquearForm(lista=lista)
    if user.tipo == 2:
        return render(request, 'core/desbloquear.html', {'form': form})
    return render(request, 'core/index.html')


def desmarcar(request, get_id):
    """Desmarca consulta."""
    marc = models.Marcacao.objects.get(id=get_id)
    marc.ativo = False
    marc.save()
    return redirect('core.consultas')
