from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='core.index'),
    path('cadastro', views.cadastro, name='core.cadastro'),
]
