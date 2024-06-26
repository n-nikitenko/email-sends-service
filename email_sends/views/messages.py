from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from email_sends.models import Message


class MessageListView(ListView):
    model = Message
    paginate_by = 10


class MessageCreateView(CreateView):
    model = Message

    fields = ['theme', 'body']
    success_url = reverse_lazy('email_sends:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['theme', 'body']
    success_url = reverse_lazy('email_sends:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('email_sends:message_list')


class MessageDetailView(DetailView):
    model = Message
