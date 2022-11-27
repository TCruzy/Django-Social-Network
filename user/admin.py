from django.contrib import admin
from user.models import User
from adminsortable2.admin import SortableAdminMixin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'profile_picture',
        'order',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = (
        'first_name',
        'last_name',
        'email',
    )
    fieldsets = (
        (
            _('User'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'profile_picture',
                    'password',
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

