from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, *args, **kwargs):
        cns = kwargs['cns']
        password = kwargs['password']
        kwargs.pop('password')

        if not cns:
            raise ValueError('CNS?')

        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(**kwargs)
        user.nascimento = '2001-01-01'
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ACS(models.Model):
    nome = models.CharField('Nome', max_length=50)
    equipe = models.IntegerField('Equipe')
    micro = models.IntegerField('Micro')

    class Meta:
        verbose_name = 'ACS'
        verbose_name_plural = 'ACS'

    def __str__(self):
        return self.nome


class Cadastro(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'cns'
    objects = UserManager()

    cns = models.CharField('CNS', max_length=15, unique=True)
    nome = models.CharField('Nome Completo', max_length=100)
    nascimento = models.DateField('Data de Nascimento', null=True)
    endereco = models.CharField('Endereço', max_length=100)
    telefone = models.CharField('Telefone', max_length=15)
    acs = models.ForeignKey(ACS, on_delete=models.CASCADE, verbose_name='ACS',
                            null=True)
    is_staff = models.BooleanField('Staff', default=False)
    create_on = models.DateField('Criado em:', auto_now_add=True)
    update_on = models.DateField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Cadastro'
        verbose_name_plural = 'Cadastros'

    def __str__(self):
        return self.nome
