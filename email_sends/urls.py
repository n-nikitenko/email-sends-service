from django.urls import path
from django.views.generic import TemplateView

from email_sends.apps import EmailSendsConfig
from email_sends.views import ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView

app_name = EmailSendsConfig.name

urlpatterns = [
    path('', TemplateView.as_view(template_name="email_sends/base.html"), name='home'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='edit_client'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='delete_client'),
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),
]
