from django.contrib.auth.models import User
from rest_framework import serializers

from AppointmentandBooking.models import Booking, Appointment
from Chat.models import Chat
from Notification.models import Notification
from RateandReview.models import Review, Rate
from Users.models import Users, ImageGallery, VideoGallery, UsersImage, UsersVideo, CheckList
from Vendor.models import Vendor, Category, Pricing, VendorImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class VendorSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Vendor
        exclude = ['slug', 'status', 'login_id']


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        exclude = ['login_id', 'slug']


class SendMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['message', 'user', 'vendor', 'sender']


class PricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pricing
        fields = ['id', 'title', 'detail', 'value']


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id', 'start_time', 'end_time', 'date', 'status', 'expired', 'declined', 'canceled', 'vendor', 'user']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'start_time', 'date', 'end_time', 'status', 'expired', 'declined', 'canceled', 'vendor', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest')
    user_name = serializers.CharField(source='user')

    class Meta:
        model = Review
        fields = ['id', 'review', 'guest_name', 'user_name']


class VendorImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorImage
        fields = ['id', 'image_location']


class VendorChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        exclude = ['user', 'vendor']


class RateVendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ['id', 'rate_value']


class RateVendorSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = '__all__'


class ReviewVendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'review']


class ReviewVendorSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class UsersImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageGallery
        fields = ['id', 'image_location']


class UsersVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoGallery
        fields = ['id', 'video_location']


class UsersImageUploadSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = UsersImage
        fields = ['id', 'image_location', 'user']


class UsersVideoUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersVideo
        fields = ['id', 'video_location', 'user']


class LoginUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    old_pass = serializers.CharField()
    new_pass = serializers.CharField()
    con_pass = serializers.CharField()


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'title', 'notification_date', 'read_status']


class BookingSerializerOne(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor')

    class Meta:
        model = Booking
        fields = ['id', 'start_time', 'end_time', 'date', 'status', 'expired', 'declined', 'canceled', 'vendor_name']


class AppointmentSerializerOne(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor')

    class Meta:
        model = Appointment
        fields = ['id', 'start_time', 'date', 'end_time', 'status', 'expired', 'declined', 'canceled', 'vendor_name']


class CheckListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckList
        fields = '__all__'


class UserChatSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = Chat
        fields = '__all__'


class PricingSerializerOne(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = Pricing
        fields = '__all__'

