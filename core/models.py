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


class Equipe(models.Model):
    nome = models.CharField('Nome', max_length=50)
    ine = models.CharField('INE', max_length=10)
    area = models.PositiveIntegerField('Área')

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'

    def __str__(self):
        return '{} - {}'.format(self.area, self.nome)


class Odontologo(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'cns'
    cns = models.CharField('CNS', max_length=18, unique=True)
    nome = models.CharField('Nome Completo', max_length=100)
    equipe = models.ForeignKey(
        Equipe, on_delete=models.CASCADE, verbose_name='Equipe'
    )
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Odontólogo'
        verbose_name_plural = 'Odontólogos'

    def __str__(self):
        return '{} - {}'.format(self.equipe, self.nome)


class ACS(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'cns'
    cns = models.CharField('CNS', max_length=18, unique=True)
    nome = models.CharField('Nome Completo', max_length=100)
    equipe = models.ForeignKey(
        Equipe, on_delete=models.CASCADE, verbose_name='Equipe'
    )
    micro = models.PositiveIntegerField('Micro')
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'ACS'
        verbose_name_plural = 'ACS'

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
        ACS, on_delete=models.CASCADE, verbose_name='ACS'
    )
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return '{} - {}'.format(self.cns, self.nome)


class Marcacao(models.Model):
    M = (
        ('1', 'Consulta de rotina'),
        ('2', 'Limpeza'),
        ('3', 'Tratamento clínico (Extração/Restauração)'),
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
        Usuario, editable=False, on_delete=models.CASCADE,
        verbose_name='Usuário'
    )

    class Meta:
        verbose_name = 'Marcação'
        verbose_name_plural = 'Marcações'

    def __str__(self):
        return '{} - {}'.format(self.user.cns, self.user.nome)
