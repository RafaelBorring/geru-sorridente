from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class ACS(models.Model):
    nome = models.CharField('Nome', max_length=50)
    equipe = models.IntegerField('Equipe')
    micro = models.IntegerField('Micro')

    class Meta:
        verbose_name = 'ACS'
        verbose_name_plural = 'ACS'

    def __str__(self):
        return self.nome


class Cadastro(AbstractBaseUser):
    USERNAME_FIELD = 'cns'

    cns = models.CharField('CNS', max_length=15)
    nome = models.CharField('Nome Completo', max_length=100)
    nascimento = models.DateField('Data de Nascimento')
    endereco = models.CharField('Endereço', max_length=100)
    telefone = models.CharField('Telefone', max_length=15)
    acs = models.ForeignKey(ACS, on_delete=models.CASCADE, verbose_name='ACS')
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Cadastro'
        verbose_name_plural = 'Cadastros'

    def __str__(self):
        return self.nome
