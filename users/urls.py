from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, PasswordResetView, UserDetailView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login', LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:email>/<str:token>/', email_verification, name="email-confirm"),
    path('reset-password', PasswordResetView.as_view(template_name="users/reset_password.html"), name='reset-password'),
    path('reset-password/done/',
         TemplateView.as_view(template_name="users/password_reset_done.html"),
         name='password-reset-done'),
    path('profile', UserDetailView.as_view(), name='user-profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='profile-edit')
]
