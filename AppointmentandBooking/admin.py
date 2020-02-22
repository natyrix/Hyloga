from django.contrib import admin
from .models import Appointment, Booking


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'user', 'status', 'date')
    list_display_links = ('id', 'vendor')
    list_filter = ('date', 'vendor')
    search_fields = ('vendor', 'user',)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'user', 'status', 'date')
    list_display_links = ('id', 'vendor')
    list_filter = ('date', 'vendor')
    search_fields = ('vendor', 'user',)


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Booking, BookingAdmin)