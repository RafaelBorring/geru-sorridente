from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class Equipes(models.Model):
    nome = models.CharField('Nome', max_length=50)
    ine = models.CharField('INE', max_length=10)
    area = models.CharField('Área', max_length=4)

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'

    def __str__(self):
        return '{} - {}'.format(self.area, self.nome)


class ACS(models.Model):
    nome = models.CharField('Nome', max_length=50)
    equipe = models.ForeignKey(
        Equipes, on_delete=models.CASCADE, verbose_name='Equipe')
    micro = models.IntegerField('Micro')

    class Meta:
        verbose_name = 'ACS'
        verbose_name_plural = 'ACS'
        ordering = ['equipe', 'micro', 'nome']

    def __str__(self):
        return '{} - {}'.format(self.micro, self.nome)


class UserManager(BaseUserManager):

    def create_user(self, *args, **kwargs):
        password = kwargs['password']
        kwargs.pop('password')
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(**kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Cadastro(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'cns'
    REQUIRED_FIELDS = ['nome', 'nascimento']
    objects = UserManager()
    cns = models.CharField('CNS', max_length=18, unique=True)
    nome = models.CharField('Nome Completo', max_length=100)
    nascimento = models.DateField('Data de Nascimento')
    endereco = models.CharField('Endereço', max_length=100)
    telefone = models.CharField('Telefone', max_length=15)
    acs = models.ForeignKey(ACS, on_delete=models.CASCADE, verbose_name='ACS',
                            null=True)
    is_odonto = models.BooleanField('Odontólogo', default=False)
    is_staff = models.BooleanField('Staff', default=False)
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Cadastro'
        verbose_name_plural = 'Cadastros'

    def __str__(self):
        return '{} - {}'.format(self.cns, self.nome)


class Marcacao(models.Model):
    M = (
        ('1', 'Consulta de rotina'),
        ('2', 'Limpeza'),
        ('3', 'Tratamento Clínico (Extração/Restauração)'),
        ('4', 'Prótese'),
        ('5', 'Outros motivos')
    )
    P = (
        ('1', 'Sim'),
        ('2', 'Não')
    )

    data = models.DateField('Data')
    motivo = models.CharField('Motivo da consulta', max_length=1, choices=M)
    protese = models.CharField('Usa prótese', max_length=1, choices=P)
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE,
        verbose_name='Usuário')

    class Meta:
        verbose_name = 'Marcação'
        verbose_name_plural = 'Marcações'

    def __str__(self):
        return '{} - {}'.format(self.user.cns, self.user.nome)


class Odonto(models.Model):
    nome = models.ForeignKey(
        Cadastro, on_delete=models.CASCADE, verbose_name='Nome')
    equipe = models.ForeignKey(
        Equipes, on_delete=models.CASCADE, verbose_name='Equipe')

    class Meta:
        verbose_name = 'Odontólogo'
        verbose_name_plural = 'Odontólogos'

    def __str__(self):
        return '{} - {}'.format(self.equipe, self.nome)
