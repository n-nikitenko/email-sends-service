from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from email_sends.models import Message
from email_sends.views.mailing import IsCouldBeChangedMixin, IsCouldBeDetailMixin


class MessageListView(ListView):
    model = Message
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.model.objects.none()
        return super().get_queryset().filter(creator=self.request.user)



class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message

    fields = ['theme', 'body']
    success_url = reverse_lazy('email_sends:message_list')

    def form_valid(self, form):
        if form.is_valid():
            message = form.save()
            message.creator = self.request.user
            message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, IsCouldBeChangedMixin, UpdateView):
    model = Message
    fields = ['theme', 'body']
    success_url = reverse_lazy('email_sends:message_list')


class MessageDeleteView(LoginRequiredMixin, IsCouldBeChangedMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('email_sends:message_list')


class MessageDetailView(IsCouldBeDetailMixin, DetailView):
    model = Message
