"""
Admin django.
"""
from django.contrib import admin
from django.contrib.auth.hashers import make_password

from core import models


class OdontologoAdmin(admin.ModelAdmin):
    """Odontólogo no admin."""

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.save()

    class Media:
        js = [
            'jquery/js/jquery.slim.min.js',
            'jquery/js/jquery.mask.min.js',
            'core/js/index.js'
        ]


class ACSAdmin(admin.ModelAdmin):
    """ACS no admin."""

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.save()

    class Media:
        js = [
            'jquery/js/jquery.slim.min.js',
            'jquery/js/jquery.mask.min.js',
            'core/js/index.js'
        ]


admin.site.register(models.Unidade)
admin.site.register(models.Equipe)
admin.site.register(models.Odontologo, OdontologoAdmin)
admin.site.register(models.ACS, ACSAdmin)
admin.site.register(models.Usuario)
admin.site.register(models.Marcacao)
admin.site.register(models.Motivo)
admin.site.register(models.Agenda)
