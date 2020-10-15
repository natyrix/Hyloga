from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path

from .models import Users, CheckList, UsersImage, UsersVideo, VideoGallery, ImageGallery, Budget, WishList
from django.utils.html import format_html


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


class UsersVideoAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve_vid/<int:vid_id>', self.approve_one, name='approve_one'),
        ]
        return custom_urls + urls

    list_display = ('user', 'video_location', 'is_approved', 'approve_this')
    list_display_links = ('user',)
    search_fields = ('user',)
    actions = ['approve']

    def approve(self, request, queryset):
        for vid in queryset:
            if not vid.status:
                u_vid = VideoGallery(user=vid.user, video_location=vid.video_location)
                u_vid.save()
                vid.status = True
                vid.save()

    def approve_this(self, obj):
        return format_html(
            f'<a style="float: none" href="approve_vid/{obj.id}" class="a-button a-button-primary">Approve</a>'
        ) if not obj.status else ""

    def is_approved(self, obj):
        return format_html(
            f'<span style="color: Green">Approved</span>'
        ) if obj.status else format_html(
            f'<span style="color: Red">Not Approved</span>'
        )
    is_approved.short_description = "Approved status"

    def approve_one(self, request, vid_id):
        vid = UsersVideo.objects.filter(pk=vid_id)
        if vid.exists():
            vid = vid.first()
            if not vid.status:
                u_vid = VideoGallery(user=vid.user, video_location=vid.video_location)
                u_vid.save()
                vid.status = True
                vid.save()
        else:
            return HttpResponse("Page Not Found")
        return HttpResponseRedirect("../")


class UsersImageAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:img_id>', self.approve_one, name='approve_one'),
        ]
        return custom_urls + urls

    list_display = ('user', 'image_location', 'is_approved', 'approve_this')
    list_display_links = ('user',)
    search_fields = ('user',)
    actions = ['approve']

    def approve(self, request, queryset):
        for img in queryset:
            if not img.status:
                u_img = ImageGallery(user=img.user, image_location=img.image_location)
                u_img.save()
                img.status = True
                img.save()

    def approve_this(self, obj):
        return format_html(
            f'<a style="float: none" href="approve/{obj.id}" class="a-button a-button-primary">Approve</a>'
        ) if not obj.status else ""

    def is_approved(self, obj):
        return format_html(
            f'<span style="color: Green">Approved</span>'
        ) if obj.status else format_html(
            f'<span style="color: Red">Not Approved</span>'
        )
    is_approved.short_description = "Approved status"

    def approve_one(self, request, img_id):
        img = UsersImage.objects.filter(pk=img_id)
        if img.exists():
            img = img.first()
            if not img.status:
                u_img = ImageGallery(user=img.user, image_location=img.image_location)
                u_img.save()
                img.status = True
                img.save()
        else:
            return HttpResponse("Page Not Found")
        return HttpResponseRedirect("../")


class ImageGalleyAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_location')
    # list_display_links = ('user',)
    # list_editable = ('status',)
    search_fields = ('user',)


class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_location')
    search_fields = ('user',)


admin.site.register(Users, UsersAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(UsersImage, UsersImageAdmin)
admin.site.register(UsersVideo, UsersVideoAdmin)
admin.site.register(VideoGallery, VideoGalleryAdmin)
admin.site.register(ImageGallery, ImageGalleyAdmin)
admin.site.register(Budget, BudgetAdmin)
