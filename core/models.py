from calendar import different_locale, month_name
from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        password = kwargs['password']
        kwargs.pop('password')
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Unidade(models.Model):
    nome = models.CharField('Nome', max_length=50)
    cnes = models.CharField('CNES', max_length=7)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering = ['nome']

    def __str__(self):
        return '{} - {}'.format(self.cnes, self.nome)


class Equipe(models.Model):
    unidade = models.ForeignKey(
        'Unidade', on_delete=models.CASCADE, verbose_name='Unidade'
    )
    nome = models.CharField('Nome', max_length=50)
    ine = models.CharField('INE', max_length=10)
    area = models.PositiveIntegerField('Área')

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'
        ordering = ['area']

    def __str__(self):
        return '{:04d} - {}'.format(self.area, self.nome)


class Odontologo(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'cns'
    cns = models.CharField('CNS', max_length=18, unique=True)
    nome = models.CharField('Nome Completo', max_length=100)
    equipe = models.ForeignKey(
        'Equipe', on_delete=models.CASCADE, verbose_name='Equipe'
    )
    tipo = models.PositiveIntegerField('Tipo de Acesso', default=1)
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Acesso ao Admin', default=False)
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Odontólogo'
        verbose_name_plural = 'Odontólogos'
        ordering = ['equipe__area', 'nome']

    def __str__(self):
        return '{} - {}'.format(self.equipe, self.nome)


class ACS(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'cns'
    cns = models.CharField('CNS', max_length=18, unique=True)
    nome = models.CharField('Nome Completo', max_length=100)
    equipe = models.ForeignKey(
        'Equipe', on_delete=models.CASCADE, verbose_name='Equipe'
    )
    micro = models.PositiveIntegerField('Micro')
    tipo = models.PositiveIntegerField('Tipo de Acesso', default=2)
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Acesso ao Admin', default=False)
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'ACS'
        verbose_name_plural = 'ACS'
        ordering = ['equipe__area', 'micro', 'nome']

    def __str__(self):
        return '{} - {}'.format(self.equipe, self.nome)


class Usuario(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'cns'
    cns = models.CharField('CNS', max_length=18, unique=True)
    nome = models.CharField('Nome Completo', max_length=100)
    nascimento = models.DateField('Data de Nascimento')
    endereco = models.CharField('Endereço', max_length=100)
    telefone = models.CharField('Telefone', max_length=15)
    acs = models.ForeignKey(
        'ACS', on_delete=models.CASCADE, verbose_name='ACS'
    )
    tipo = models.PositiveIntegerField('Tipo de Acesso', default=3)
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Acesso ao Admin', default=False)
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nome']

    def __str__(self):
        return '{} - {}'.format(self.cns, self.nome)


class Marcacao(models.Model):
    P = (
        ('1', 'Sim'),
        ('0', 'Não')
    )
    data = models.DateField('Data')
    motivo = models.ForeignKey(
        'Motivo', on_delete=models.CASCADE, verbose_name='Motivo',
        default=False
    )
    protese = models.CharField(
        'Usa prótese', max_length=1, choices=P, default=False
    )
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)
    user = models.ForeignKey(
        'Usuario', editable=False, on_delete=models.CASCADE,
        verbose_name='Usuário'
    )

    class Meta:
        verbose_name = 'Marcação'
        verbose_name_plural = 'Marcações'
        ordering = ['-data']

    def __str__(self):
        return '{} - {} - {}'.format(self.data, self.user.cns, self.user.nome)


class Motivo(models.Model):
    motivo = models.CharField('Motivo', max_length=50)

    class Meta:
        verbose_name = 'Motivo'
        verbose_name_plural = 'Motivos'
        ordering = ['motivo']

    def __str__(self):
        return self.motivo


class Agenda(models.Model):
    mes = models.PositiveIntegerField('Mês de Referência')
    ano = models.PositiveIntegerField(
        'Ano de Referência', default=date.today().year
    )
    dia = models.CharField('Dias da Semana', max_length=35)
    vaga = models.PositiveIntegerField('Quantidade de Vagas por ACS')
    tempo = models.PositiveIntegerField('Tempo Médio da Consulta', default=20)
    equipe = models.ForeignKey(
        'Equipe', on_delete=models.CASCADE, verbose_name='Equipe'
    )

    class Meta:
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'
        ordering = ['mes', 'ano']

    def __str__(self):
        with different_locale('pt_BR.UTF-8'):
            return '{} de {}'.format(month_name[self.mes].title(), self.ano)
