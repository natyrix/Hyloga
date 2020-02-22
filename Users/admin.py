from django.contrib import admin
from .models import Users, CheckList, UsersImage, UsersVideo, VideoGallery, ImageGallery, Budget, WishList


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'fiance_first_name', 'wedding_date')
    list_display_links = ('id', 'first_name')
    list_filter = ('wedding_date', )
    search_fields = ('first_name', 'fiance_first_name')
    list_per_page = 20


class CheckListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_number', 'date_and_time', 'status')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    list_per_page = 20


class WishListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'is_ticked')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'content')
    list_per_page = 20


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount')
    list_display_links = ('id', 'user')
    search_fields = ('user',)


admin.site.register(Users, UsersAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(UsersImage)
admin.site.register(UsersVideo)
admin.site.register(VideoGallery)
admin.site.register(ImageGallery)
admin.site.register(Budget, BudgetAdmin)
