from django.contrib import admin
from .models import Vendor, VendorImage, Category, Pricing


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'slug', 'status', 'category')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'status')
    search_fields = ('name',)
    list_per_page = 20


class PricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value', 'detail', 'vendor')
    list_display_links = ('id', 'title')
    search_fields = ('vendor', 'title')
    list_filter = ('vendor',)
    list_per_page = 20


admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorImage)
admin.site.register(Category)
admin.site.register(Pricing, PricingAdmin)