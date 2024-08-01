import secrets
from smtplib import SMTPSenderRefused

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, UpdateView, DetailView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import RegisterForm
from users.models import User


class UserCreateView(CreateView):
    """представление для регистрации пользователя"""

    model = User
    form_class = RegisterForm

    @staticmethod
    def send_confirmation_email(confirm_url, email):
        """отправка письма для подтверждения email пользователя"""

        try:
            send_mail(
                'Подтверждение электронной почты в сервисе Florist',
                f'Для завершения регшистрации перейдите по ссылке {confirm_url}.',
                EMAIL_HOST_USER,
                [email],
                fail_silently=False, )
        except SMTPSenderRefused as e:
            pass  # TODO: logging error

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            token = secrets.token_hex(16)
            host = self.request.get_host()
            url = f"http://{host}/users/email-confirm/{user.email}/{token}/"
            user.token = token
            self.send_confirmation_email(url, user.email)
            user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:login')


def email_verification(request, email, token):
    """endpoint для подтверждения email пользователя"""

    user = User.objects.filter(email=email, token=token).first()
    if user:
        user.is_active = True
        user.token = None
        user.save()
        return render(request, 'users/verification-result.html',
                      context={'title': 'Email подтвержден.', 'is_error': False})
    return render(request, 'users/verification-result.html',
                  context={'title': 'Ошибка подтверждения email.', 'is_error': True})


class PasswordResetView(FormView):
    form_class = PasswordResetForm

    @staticmethod
    def send_password_reset_email(email, password, login_url):
        """отправка письма с новым паролем пользователя"""

        try:
            send_mail(
                'Смена пароля в сервисе Florist',
                f'Ваш новый пароль: {password}. Для входа перейдите по ссылке: {login_url}',
                EMAIL_HOST_USER,
                [email],
                fail_silently=False, )
        except SMTPSenderRefused as e:
            pass  # TODO: logging error

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                new_password = secrets.token_urlsafe(16)
                user.set_password(new_password)
                user.save()
                host = self.request.get_host()
                login_url = f"http://{host}/users/login"
                self.send_password_reset_email(user.email, new_password, login_url)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:password-reset-done')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """представление для изменения данных профиля пользователя"""

    model = User
    fields = ["email", "phone", "country", "avatar"]

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user-profile')


class UserDetailView(LoginRequiredMixin, DetailView):
    """представление для отображения данных профиля пользователя"""

    model = User

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    """представление для отображения списка пользователей"""

    model = User
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        if self.request.user.is_manager:
            return super().get_context_data(**kwargs)
        raise PermissionDenied


@login_required
def lock_user(request, user_id):
    """endpoint для блокировки пользователя"""

    if request.user.has_perm('can_change_is_active') and request.user.id != user_id:
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
        return redirect("users:user-list")
    raise PermissionDenied


@login_required
def unlock_user(request, user_id):
    """endpoint для разблокировки пользователя"""

    if request.user.has_perm('can_change_is_active') and request.user.id != user_id:
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        return redirect("users:user-list")
    raise PermissionDenied
