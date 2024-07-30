from django.views.generic import ListView

from email_sends.models import MailingLog


class MailingLogListView(ListView):
    model = MailingLog
    paginate_by = 10
    ordering = ['-last_sent']
