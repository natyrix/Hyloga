from django.contrib import admin
from .models import Rate, Review


class RateAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'rate_value', 'vendor', 'user', 'guest')
    list_display_links = ('id', 'type')
    list_filter = ('type', 'vendor')
    search_fields = ('user',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'vendor', 'user', 'guest')
    list_display_links = ('id', 'type')
    list_filter = ('type', 'vendor')
    search_fields = ('user',)


admin.site.register(Rate, RateAdmin)
admin.site.register(Review, ReviewAdmin)