from django.urls import path
from django.views.generic import TemplateView

from email_sends.apps import EmailSendsConfig
from email_sends.views import ClientListView

app_name = EmailSendsConfig.name

urlpatterns = [
    path('', TemplateView.as_view(template_name="email_sends/base.html"), name='home'),
    path('clients/', ClientListView.as_view(), name='client_list'),
]
