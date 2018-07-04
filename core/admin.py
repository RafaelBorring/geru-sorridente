from django.contrib import admin

from core import models


admin.site.register(models.Equipes),
admin.site.register(models.Odonto),
admin.site.register(models.ACS),
admin.site.register(models.Cadastro),
admin.site.register(models.Marcacao)
