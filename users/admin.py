from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'phone', 'avatar', 'is_active', 'is_staff',)
    list_filter = ('is_active',)
    search_fields = ('email', 'content',)
