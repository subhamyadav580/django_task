from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User

class AccountAdmin(BaseUserAdmin):

    list_display = ('email', 'username', 'first_name', 'last_name', 'age', 'uniqueID', 'is_staff',  'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'age', 'uniqueID', 'picture')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'age', 'uniqueID', 'picture')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, AccountAdmin)
