from django.contrib import admin
from .models import AccountType


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'Actype')
    list_display_links = ('id', 'user')
    list_filter = ('Actype',)
    search_fields = ('Actype',)


admin.site.register(AccountType, AccountAdmin)
