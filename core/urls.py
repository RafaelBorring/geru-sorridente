from django.urls import path
from django.views.generic import TemplateView as TV

urlpatterns = [
    path('', TV.as_view(template_name='core/index.html'), name='core.index'),
]
