from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField
from django.forms.utils import ErrorList

from users.models import User


class StyleFormMixin:
    error_css_class = "text-danger form-control is-invalid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = RedFontErrorList
        for _, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
            if field.required:
                field.label += " *"


class RedFontErrorList(ErrorList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class += " text-danger"


class RegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя по email и паролю"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
