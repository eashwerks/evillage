from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext, gettext_lazy as _

from app_0.models import NotificationService, VillageOfficer


class VillageOfficerCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


class VillageOfficerAdmin(UserAdmin):
    add_form = VillageOfficerCreateForm
    list_display = ('username', 'email', 'first_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'email', 'username', 'password1', 'password2',),
        }),
    )


admin.site.unregister(Group)
admin.site.register(VillageOfficer, VillageOfficerAdmin)
admin.site.register(NotificationService)
