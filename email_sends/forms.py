from django.forms import ModelForm

from email_sends.models import MailingSettings
from users.forms import StyleFormMixin


class ManagerUpdateMailingSettingsForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingSettings
        fields = ["status"]
