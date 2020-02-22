from django.contrib import admin
from .models import Chat


class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vendor', 'message', 'sent_time')
    list_display_links = ('id', 'user')
    list_filter = ('sent_time', 'user', 'vendor')
    search_fields = ('user', 'vendor', 'message')


admin.site.register(Chat, ChatAdmin)