import datetime

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models import QuerySet, Avg
from API.serializers import VendorSerializer, UsersSerializer, SendMessageSerializer, PricingSerializer, \
    BookingSerializer, AppointmentSerializer, ReviewSerializer, VendorImageSerializer, VendorChatSerializer, \
    RateVendorSerializer, RateVendorSerializer1, ReviewVendorSerializer, ReviewVendorSerializer1, UsersImageSerializer, \
    UsersVideoSerializer, UsersImageUploadSerializer, UsersVideoUploadSerializer, LoginUserUpdateSerializer, \
    ChangePasswordSerializer, NotificationSerializer, AppointmentSerializerOne, BookingSerializerOne
from AppointmentandBooking.models import Appointment, Booking
from Chat.models import sender, Chat
from Notification.models import Notification, ty
from RateandReview.models import Rate, Review
from Users.models import Users, ImageGallery, VideoGallery
from Users.views import setExpired
from Vendor.models import Vendor, Pricing, VendorImage
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


def returnUsersObjFromToken(token):
    user = Token.objects.get(key=token[1])
    users = Users.objects.filter(login_id=user.user)
    if users.exists():
        users = users.first()
        setExpired(users)
        return users
    return None


class VendorViewSet(views.APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        ratings = []
        for vendor in vendors:
            vendor_rating = Rate.objects.filter(vendor=vendor).aggregate(Avg('rate_value'))
            ratings.append(vendor_rating['rate_value__avg'])
        return Response({"data": serializer.data, "ratings": ratings})


class UsersViewSet(views.APIView):

    def get(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            serializer = UsersSerializer(users)
            return Response(serializer.data)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            date_time_obj = datetime.datetime.strptime(request.data['wedding_date'], '%Y-%m-%d %H:%M:%S.%f')
            data = {
                "first_name": request.data['first_name'],
                "last_name": request.data['last_name'],
                "email": request.data['email'],
                "role": request.data['role'],
                "wedding_date": date_time_obj.date(),
                "fiance_first_name": request.data['fiance_first_name'],
                "fiance_last_name": request.data['fiance_last_name'],
                "fiance_email": request.data['fiance_email'],
            }
            login_user = User.objects.get(pk=users.login_id.id)
            login_data = {
                "username": str(request.data['email']).split('@')[0],
                "email": str(request.data['email'])
            }
            serializer = UsersSerializer(users, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                login_serializer = LoginUserUpdateSerializer(login_user, data=login_data, partial=True)
                if login_serializer.is_valid():
                    login_serializer.save()
                    return Response({"message": "Profile updated successfully"})
                else:
                    print(login_serializer.errors)
                    return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(serializer.errors)
                return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class SendMessageViewSet(views.APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            data = {
                'message': request.data['message'],
                'vendor': int(pk),
                'user': users.id,
                'sender': sender[1][0]
            }
            serializer = SendMessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Message sent successfully"}, )
            else:
                print(serializer.errors)
                return Response({"message": "Invalid data provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class VendorPricingViewSet(views.APIView):

    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                pricings = Pricing.objects.filter(vendor=vendor)
                if pricings.exists():
                    serializer = PricingSerializer(pricings, many=True)
                    return Response(serializer.data)
                else:
                    return Response({"message": "No pricing found for this vendor"},
                                    status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class ApptViewSet(views.APIView):
    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                appt = Appointment.objects.filter(vendor=vendor, user=users)
                if appt.exists():
                    aptserializer = AppointmentSerializer(appt, many=True)
                    return Response(aptserializer.data)
                else:
                    return Response({"message": "You have no appointment with this vendor"},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class BookingViewSet(views.APIView):
    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                bkg = Booking.objects.filter(vendor=vendor, user=users)
                if bkg.exists():
                    serializer = BookingSerializer(bkg, many=True)
                    return Response(serializer.data)
                else:
                    return Response({"message": "You have no booking with this vendor"},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class ReviewViewSet(views.APIView):
    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                reviews = Review.objects.filter(vendor=vendor)
                if reviews.exists():
                    serializer = ReviewSerializer(reviews, many=True)
                    return Response(serializer.data)
                else:
                    return Response({"message": "This vendor has no reviews"},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class VendorImageViewSet(views.APIView):
    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                images = VendorImage.objects.filter(vendor=vendor)
                if images.exists():
                    serializer = VendorImageSerializer(images, many=True)
                    return Response(serializer.data)
                else:
                    return Response({"message": "This vendor has no images"},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class VendorChatViewSet(views.APIView):
    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                chats = Chat.objects.filter(vendor=vendor, user=users)
                if chats.exists():
                    serializer = VendorChatSerializer(chats, many=True)
                    return Response(serializer.data)
                else:
                    return Response({"message": "You have no recent chat with this vendor"},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class VendorRateViewSet(views.APIView):
    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                rating = Rate.objects.filter(vendor=vendor, user=users)
                if rating.exists():
                    rating = rating.first()
                    serializer = RateVendorSerializer(rating)
                    return Response(serializer.data)
                else:
                    return Response({"message": "No rating found"},
                                    status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                rating = Rate.objects.filter(vendor=vendor, user=users)
                rat_val = str(request.data['rate_val']).split('.')
                rat_val = int(rat_val[0])
                if rating.exists():
                    rating = rating.first()
                    d = {"rate_value": rat_val}
                    rating_serializer = RateVendorSerializer1(rating, data=d, partial=True)
                    if rating_serializer.is_valid():
                        rating_serializer.save()
                        return Response({
                            "message": "Rating updated successfully"
                        })
                    else:
                        print(rating_serializer.errors)
                        return Response({
                            "message": "Invalid data provided"
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    d = {
                        'rate_value': rat_val,
                        'type': "Vendor",
                        'vendor': vendor.id,
                        'user': users.id
                    }
                    rating_serializer = RateVendorSerializer1(data=d)
                    if rating_serializer.is_valid():
                        rating_serializer.save()
                        return Response({
                            'message': 'Rated successfully'
                        })
                    else:
                        print(rating_serializer.errors)
                        return Response({
                            "message": "Invalid data provided"
                        }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class VendorReviewViewSet(views.APIView):
    def get(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                review = Review.objects.filter(vendor=vendor, user=users)
                if review.exists():
                    review = review.first()
                    serializer = ReviewVendorSerializer(review)
                    return Response(serializer.data)
                else:
                    return Response({"message": "No review found"},
                                    status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vendor = Vendor.objects.filter(pk=pk)
            if vendor.exists():
                vendor = vendor.first()
                review = Review.objects.filter(vendor=vendor, user=users)
                rev = str(request.data['review'])
                if review.exists():
                    review = review.first()
                    d = {"review": rev}
                    review_serializer = ReviewVendorSerializer1(review, data=d, partial=True)
                    if review_serializer.is_valid():
                        review_serializer.save()
                        return Response({
                            "message": "Review updated successfully"
                        })
                    else:
                        print(review_serializer.errors)
                        return Response({
                            "message": "Invalid data provided"
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    d = {
                        'review': rev,
                        'type': "Vendor",
                        'vendor': vendor.id,
                        'user': users.id
                    }
                    review_serializer = ReviewVendorSerializer1(data=d)
                    if review_serializer.is_valid():
                        review_serializer.save()
                        return Response({
                            'message': 'Reviewed successfully'
                        })
                    else:
                        print(review_serializer.errors)
                        return Response({
                            "message": "Invalid data provided"
                        }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Unable to fetch data"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class UserImageViewSet(views.APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            images = ImageGallery.objects.filter(user=users)
            if images.exists():
                serializer = UsersImageSerializer(images, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "You have no image uploads"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            img_data = {
                'image_location': request.data['file_field'],
                'user': users.id
            }
            img_serializer = UsersImageUploadSerializer(data=img_data)
            if img_serializer.is_valid():
                img_serializer.save()
                return Response("Upload successful")
            else:
                print(img_serializer.errors)
                return Response("Error occurred",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            assert int(pk), "Invalid id provided"
            image = ImageGallery.objects.filter(pk=int(pk), user=users)
            if image.exists():
                image = image.first()
                image.delete()
                return Response({
                    "message": "Image removed successfully"
                })
            else:
                Response({"message": "Image not found"},
                         status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class UserVideoViewSet(views.APIView):
    def get(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            videos = VideoGallery.objects.filter(user=users)
            if videos.exists():
                serializer = UsersVideoSerializer(videos, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "You have no video uploads"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            vid_data = {
                'video_location': request.data['file_field'],
                'user': users.id
            }
            vid_serializer = UsersVideoUploadSerializer(data=vid_data)
            if vid_serializer.is_valid():
                # vid_serializer.save()
                return Response("Upload successful")
            else:
                print(vid_serializer.errors)
                return Response("Error occurred",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            assert int(pk), "Invalid id provided"
            video = VideoGallery.objects.filter(pk=int(pk), user=users)
            if video.exists():
                video = video.first()
                # video.delete()
                return Response({
                    "message": "Video removed successfully"
                })
            else:
                Response({"message": "Video not found"},
                         status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class ChangePasswordViewSet(views.APIView):

    def patch(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            user = User.objects.get(pk=users.login_id.id)
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                new_pass = serializer.data.get('new_pass')
                con_pass = serializer.data.get('con_pass')
                old_pass = serializer.data.get('old_pass')
                if new_pass == con_pass:
                    if old_pass != new_pass:
                        if user.check_password(old_pass):
                            user.set_password(new_pass)
                            user.save()
                            return Response({
                                'message': 'Password Updated Successfully'
                            })
                        else:
                            return Response({"message": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            'message': 'Old password is the same as new password'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'message': 'Passwords should match'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(serializer.errors)
                return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class NotificationViewSet(views.APIView):
    def get(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            notifications = Notification.objects.filter(user=users, type=ty[1][0]).order_by('-id')
            if notifications.exists():
                serializer = NotificationSerializer(notifications, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "No notifications"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class UserAppointmentsViewSet(views.APIView):
    def get(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            appointments = Appointment.objects.filter(user=users).order_by('-id')
            if appointments.exists():
                serializer = AppointmentSerializerOne(appointments, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "You have no appointments"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            appointment = Appointment.objects.filter(user=users, pk=pk)
            if appointment.exists():
                data = {
                    "canceled": True
                }
                appointment = appointment.first()
                serializer = AppointmentSerializer(appointment, data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Appointment canceled"})
                else:
                    return Response({"message": "Invalid data provided"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Appointment not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)


class UserBookingsViewSet(views.APIView):
    def get(self, request):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            bookings = Booking.objects.filter(user=users).order_by('-id')
            if bookings.exists():
                serializer = BookingSerializerOne(bookings, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "You have no bookings"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        users = returnUsersObjFromToken(str(request.META.get('HTTP_AUTHORIZATION')).split(" "))
        if users is not None:
            booking = Booking.objects.filter(user=users, pk=pk)
            if booking.exists():
                data = {
                    "canceled": True
                }
                booking = booking.first()
                serializer = BookingSerializer(booking, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Booking canceled"})
                else:
                    return Response({"message": "Invalid data provided"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Appointment not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication Failed"},
                            status=status.HTTP_403_FORBIDDEN)
