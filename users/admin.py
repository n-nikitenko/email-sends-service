from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'phone', 'avatar', 'is_active', 'is_staff',)
    list_filter = ('is_active',)
    search_fields = ('email', 'content',)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_manager

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_manager

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_manager

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_manager


admin.site.unregister(Group)


@admin.register(Group)
class UserGroupAdmin(GroupAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
