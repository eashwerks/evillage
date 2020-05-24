from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group, User

from app_0.models import NotificationService, VillageOfficer

admin.site.unregister(Group)
admin.site.register(NotificationService)
admin.site.register(VillageOfficer)