from django.shortcuts import render
from django.views.generic import ListView

from email_sends.models import Client


class ClientListView(ListView):
    model = Client
