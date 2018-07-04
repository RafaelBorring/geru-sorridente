from django.contrib.auth import views as auth_views
from django.urls import path

from core import views

urlpatterns = [
    path('login/', auth_views.login, name='auth.login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='auth.logout'),
    path('', views.index, name='core.index'),
    path('cadastro/', views.cadastro, name='core.cadastro'),
    path('calendario/', views.calendario, name='core.calendario'),
    path('marcacao/<int:ano>/<int:mes>/<int:dia>',
         views.marcacao, name='core.marcacao')
]
