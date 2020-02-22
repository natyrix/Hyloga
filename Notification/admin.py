from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'vendor', 'type', 'notification_date')
    list_display_links = ('id', 'title')
    list_filter = ('vendor', 'user')
    search_fields = ('user', 'vendor', 'type')


admin.site.register(Notification, NotificationAdmin)