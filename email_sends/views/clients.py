from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from email_sends.models import Client
from email_sends.views.mailing import IsCouldBeChangedMixin, IsCouldBeDetailMixin


class ClientListView(ListView):
    model = Client
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.model.objects.none()
        return super().get_queryset().filter(creator=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client

    fields = ['name', 'email', 'comment']
    success_url = reverse_lazy('email_sends:client_list')

    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            client.creator = self.request.user
            client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, IsCouldBeChangedMixin, UpdateView):
    model = Client
    fields = ['name', 'email', 'comment']
    success_url = reverse_lazy('email_sends:client_list')


class ClientDeleteView(LoginRequiredMixin, IsCouldBeChangedMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('email_sends:client_list')


class ClientDetailView(IsCouldBeDetailMixin, DetailView):
    model = Client
