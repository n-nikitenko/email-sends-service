from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from email_sends.forms import ManagerUpdateMailingSettingsForm
from email_sends.models import MailingSettings, Message, Client
from email_sends.services import process_mailing


# from email_sends.services import process_mailing
class IsCouldBeChangedMixin:
    def get_form_class(self):
        if self.request.user == self.get_object().creator:
            return super().get_form_class()
        raise PermissionDenied


class IsCouldBeDetailMixin:
    def get_context_data(self, **kwargs):
        if self.request.user == self.get_object().creator or self.request.user.is_manager:
            return super().get_context_data(**kwargs)
        raise PermissionDenied


class MailingSettingsListView(ListView):
    model = MailingSettings
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.model.objects.none()
        if self.request.user.is_manager:
            return super().get_queryset()
        return super().get_queryset().filter(creator=self.request.user)


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings

    fields = ['name', 'start_at', 'stop_at', 'frequency', 'clients', 'message']
    success_url = reverse_lazy('email_sends:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['message'].queryset = Message.objects.filter(creator=self.request.user)
        context['form'].fields['clients'].queryset = Client.objects.filter(creator=self.request.user)
        return context

    def get_form(self, form_class=None):
        """add date picker in forms"""
        form = super(MailingSettingsCreateView, self).get_form(form_class)
        form.fields['start_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"})
        form.fields['stop_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"})

        return form

    def form_valid(self, form):
        if form.is_valid():
            mailing = form.save()
            mailing.creator = self.request.user
            mailing.save()
            process_mailing(mailing)  # отправка рассылки при необходимости
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, IsCouldBeChangedMixin, UpdateView):
    model = MailingSettings
    fields = ['name', 'start_at', 'stop_at', 'frequency', 'clients', 'message']
    success_url = reverse_lazy('email_sends:mailing_list')

    def get_form_class(self):
        if self.request.user == self.get_object().creator:
            return super().get_form_class()
        if self.request.user.is_manager:
            return ManagerUpdateMailingSettingsForm
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.creator == self.request.user:
            context['form'].fields['message'].queryset = Message.objects.filter(creator=self.request.user)
            context['form'].fields['clients'].queryset = Client.objects.filter(creator=self.request.user)
        return context

    def get_form(self, form_class=None):
        """add date picker in forms"""
        form = super(MailingSettingsUpdateView, self).get_form(form_class)
        if self.object.creator == self.request.user:
            form.fields['start_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M",
                                                                 attrs={"type": "datetime-local"})
            form.fields['stop_at'].widget = forms.DateTimeInput(format="%Y-%m-%d %H:%M",
                                                                attrs={"type": "datetime-local"})

        return form


class MailingSettingsDeleteView(LoginRequiredMixin, IsCouldBeChangedMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('email_sends:mailing_list')


class MailingSettingsDetailView(IsCouldBeDetailMixin, DetailView):
    model = MailingSettings
