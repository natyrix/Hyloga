from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Administrator


class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'login_id', 'gender', 'phonenumber')
    list_display_links = ('id', 'login_id')


admin.site.unregister(Group)
admin.site.register(Administrator, AdministratorAdmin)