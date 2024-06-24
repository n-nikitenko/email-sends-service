from django.contrib import admin

from email_sends.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email', 'comment')
