from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from API.views import VendorViewSet, UsersViewSet, SendMessageViewSet, VendorPricingViewSet, ApptViewSet, \
    BookingViewSet, ReviewViewSet, VendorImageViewSet, VendorChatViewSet, VendorRateViewSet, VendorReviewViewSet, \
    UserImageViewSet, UserVideoViewSet, ChangePasswordViewSet, NotificationViewSet, UserAppointmentsViewSet, \
    UserBookingsViewSet

# router = DefaultRouter()
# router.register('vendors', VendorViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('login/', obtain_auth_token),
    path('vendors/', VendorViewSet.as_view()),
    path('vendors/send_msg/<int:pk>/', SendMessageViewSet.as_view()),
    path('vendors/pricings/<int:pk>/', VendorPricingViewSet.as_view()),
    path('vendors/appts/<int:pk>/', ApptViewSet.as_view()),
    path('vendors/bookings/<int:pk>/', BookingViewSet.as_view()),
    path('vendors/reviews/<int:pk>/', ReviewViewSet.as_view()),
    path('vendors/images/<int:pk>/', VendorImageViewSet.as_view()),
    path('vendors/chats/<int:pk>/', VendorChatViewSet.as_view()),
    path('vendors/rate/<int:pk>/', VendorRateViewSet.as_view()),
    path('vendors/review/<int:pk>/', VendorReviewViewSet.as_view()),
    path('users/', UsersViewSet.as_view()),
    path('users/images/', UserImageViewSet.as_view()),
    path('users/images/<int:pk>/', UserImageViewSet.as_view()),
    path('users/videos/', UserVideoViewSet.as_view()),
    path('users/change_password/', ChangePasswordViewSet.as_view()),
    path('users/notifications/', NotificationViewSet.as_view()),
    path('users/appointments/', UserAppointmentsViewSet.as_view()),
    path('users/appointments/cancel/<int:pk>/', UserAppointmentsViewSet.as_view()),
    path('users/bookings/', UserBookingsViewSet.as_view()),
    path('users/bookings/cancel/<int:pk>/', UserBookingsViewSet.as_view()),
]


