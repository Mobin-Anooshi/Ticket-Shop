from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import User,Admin,Permission_level,Driver_Documents,Vehicle
from django.contrib.auth.models import Group
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('full_name', 'email', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('full_name', 'phone_number', 'email')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'full_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('full_name', 'email')
    ordering = ('full_name',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(Permission_level)
admin.site.register(Driver_Documents)
admin.site.register(Vehicle)