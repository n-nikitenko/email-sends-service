from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from email_sends.models import Client


class ClientListView(ListView):
    model = Client
    paginate_by = 10


class ClientCreateView(CreateView):
    model = Client

    fields = ['name', 'email', 'comment']
    success_url = reverse_lazy('email_sends:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['name', 'email', 'comment']
    success_url = reverse_lazy('email_sends:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('email_sends:client_list')


class ClientDetailView(DetailView):
    model = Client
