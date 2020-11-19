from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models import QuerySet, Avg
from API.serializers import VendorSerializer, UsersSerializer, SendMessageSerializer, PricingSerializer, \
    BookingSerializer, AppointmentSerializer, ReviewSerializer, VendorImageSerializer, VendorChatSerializer, \
    RateVendorSerializer, RateVendorSerializer1, ReviewVendorSerializer, ReviewVendorSerializer1, UsersImageSerializer, \
    UsersVideoSerializer, UsersImageUploadSerializer
from AppointmentandBooking.models import Appointment, Booking
from Chat.models import sender, Chat
from RateandReview.models import Rate, Review
from Users.models import Users, ImageGallery, VideoGallery
from Vendor.models import Vendor, Pricing, VendorImage
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


def returnUsersObjFromToken(token):
    user = Token.objects.get(key=token[1])
    users = Users.objects.filter(login_id=user.user)
    if users.exists():
        users = users.first()
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
                        }, status=status.HTTP_304_NOT_MODIFIED)
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
                        }, status=status.HTTP_304_NOT_MODIFIED)
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
                        }, status=status.HTTP_304_NOT_MODIFIED)
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
                        }, status=status.HTTP_304_NOT_MODIFIED)
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
