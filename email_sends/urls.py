from django.urls import path

from email_sends.apps import EmailSendsConfig
from email_sends.views import ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView, \
    MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView, \
    MailingSettingsListView, MailingSettingsDetailView, MailingSettingsUpdateView, MailingSettingsDeleteView, \
    MailingSettingsCreateView, MailingLogListView
from email_sends.views.home import home

app_name = EmailSendsConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='edit_client'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='delete_client'),
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='edit_message'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='delete_message'),
    path('messages/create/', MessageCreateView.as_view(), name='create_message'),

    path('mailings/', MailingSettingsListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>', MailingSettingsDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/edit/', MailingSettingsUpdateView.as_view(), name='edit_mailing'),
    path('mailings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='delete_mailing'),
    path('mailings/create/', MailingSettingsCreateView.as_view(), name='create_mailing'),

    path('logs/', MailingLogListView.as_view(), name='log_list'),
]
