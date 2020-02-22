from django.contrib import admin
from .models import Guest, TickedWishList, Invitation


class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phonenumber')
    list_display_links = ('id', 'first_name')


class TickedWishListAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'wishlist')
    list_display_links = ('id', 'guest')
    search_fields = ('guest',)


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vendor', 'guest', 'address', 'starttime')
    list_display_links = ('id', 'user')
    search_fields = ('vendor', 'user', 'guest')
    list_filter = ('vendor', 'user')


admin.site.register(Guest, GuestAdmin)
admin.site.register(TickedWishList, TickedWishListAdmin)
admin.site.register(Invitation, InvitationAdmin)