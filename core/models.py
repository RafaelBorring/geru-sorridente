from calendar import day_name, different_locale
from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

with different_locale('pt_BR.UTF-8'):
    DIA_SEMANA = tuple((range(7), x.title()) for x in day_name)


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
    is_staff = models.BooleanField('Acesso Admin', default=False)
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
    is_staff = models.BooleanField('Acesso Admin', default=False)
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
    locked = models.BooleanField('Bloqueado', default=False)
    tipo = models.PositiveIntegerField('Tipo de Acesso', default=3)
    is_staff = models.BooleanField('Acesso Admin', default=False)
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
    mes = models.CharField(
        'Mês de Referência', max_length=2,
        default='{:02d}'.format(date.today().month+1)
    )
    ano = models.CharField(
        'Ano de Referência', max_length=4, default=date.today().year
    )
    dia = models.CharField(
        'Dias da Semana', max_length=2, choices=DIA_SEMANA
    )
    vaga = models.PositiveIntegerField('Quantidade de Vagas por ACS')
    tempo = models.PositiveIntegerField('Tempo Médio da Consulta', default=20)
