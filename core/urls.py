from django.contrib.auth import views as auth_views
from django.urls import path

from core import views

urlpatterns = [
    path('login/', auth_views.login, name='auth.login'),
    path('logout/', auth_views.logout, name='auth.logout'),
    path('', views.index, name='core.index'),
    path('calendario/', views.calendario, name='core.calendario'),
    path(
        'marcacao/<int:ano>/<int:mes>/<int:dia>',
        views.marcacao, name='core.marcacao'
    ),
    path('consultas/', views.consultas, name='core.consultas'),
    path('requisicao/', views.requisicao, name='core.requisicao')
]
