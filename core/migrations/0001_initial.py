# Generated by Django 2.0.4 on 2018-07-16 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ACS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cns', models.CharField(max_length=18, unique=True, verbose_name='CNS')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='Criado em:')),
                ('update_on', models.DateField(auto_now=True, verbose_name='Atualizado em:')),
            ],
            options={
                'verbose_name': 'ACS',
                'verbose_name_plural': 'ACS',
            },
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('ine', models.CharField(max_length=10, verbose_name='INE')),
                ('area', models.PositiveIntegerField(verbose_name='Área')),
            ],
            options={
                'verbose_name': 'Equipe',
                'verbose_name_plural': 'Equipes',
            },
        ),
        migrations.CreateModel(
            name='Marcacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('motivo', models.CharField(choices=[('1', 'Consulta de rotina'), ('2', 'Limpeza'), ('3', 'Tratamento Clínico (Extração/Restauração)'), ('4', 'Prótese'), ('5', 'Outros motivos')], max_length=1, verbose_name='Motivo da consulta')),
                ('protese', models.CharField(choices=[('1', 'Sim'), ('2', 'Não')], max_length=1, verbose_name='Usa prótese')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='Criado em:')),
                ('update_on', models.DateField(auto_now=True, verbose_name='Atualizado em:')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Marcação',
                'verbose_name_plural': 'Marcações',
            },
        ),
        migrations.CreateModel(
            name='Odontologo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cns', models.CharField(max_length=18, unique=True, verbose_name='CNS')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='Criado em:')),
                ('update_on', models.DateField(auto_now=True, verbose_name='Atualizado em:')),
                ('equipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Equipe', verbose_name='Equipe')),
            ],
            options={
                'verbose_name': 'Odontólogo',
                'verbose_name_plural': 'Odontólogos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cns', models.CharField(max_length=18, unique=True, verbose_name='CNS')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('endereco', models.CharField(max_length=100, verbose_name='Endereço')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='Criado em:')),
                ('update_on', models.DateField(auto_now=True, verbose_name='Atualizado em:')),
                ('acs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ACS', verbose_name='ACS')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.AddField(
            model_name='acs',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Equipe', verbose_name='Equipe'),
        ),
    ]
