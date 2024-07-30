from django.contrib import admin

from email_sends.models import Client, Message, MailingSettings, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email', 'comment')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_manager

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'body')
    list_filter = ('theme', 'body')
    search_fields = ('theme', 'body')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_manager

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_at', 'stop_at', 'frequency', 'status')
    list_filter = ('name', 'start_at', 'stop_at', 'frequency', 'status')
    search_fields = ('name', 'start_at', 'stop_at', 'frequency', 'status')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_manager

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'status', 'last_sent')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_manager

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
