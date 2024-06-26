from django import forms

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from email_sends.models import MailingSettings
# from email_sends.services import process_mailing


class MailingSettingsListView(ListView):
    model = MailingSettings
    paginate_by = 5


class MailingSettingsCreateView(CreateView):
    model = MailingSettings

    fields = ['name', 'start_at', 'stop_at', 'frequency', 'clients', 'message']
    success_url = reverse_lazy('email_sends:mailing_list')

    def get_form(self, form_class=None):
        """add date picker in forms"""
        form = super(MailingSettingsCreateView, self).get_form(form_class)
        form.fields['start_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"})
        form.fields['stop_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"})

        return form

    def form_valid(self, form):
        if form.is_valid():
            mailing = form.save()
            # process_mailing(mailing)  # отправка рассылки при необходимости
        return super().form_valid(form)


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    fields = ['name', 'start_at', 'stop_at', 'frequency', 'clients', 'message']
    success_url = reverse_lazy('email_sends:mailing_list')

    def get_form(self, form_class=None):
        """add date picker in forms"""
        form = super(MailingSettingsUpdateView, self).get_form(form_class)
        form.fields['start_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"})
        form.fields['stop_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"})

        return form


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('email_sends:mailing_list')


class MailingSettingsDetailView(DetailView):
    model = MailingSettings
