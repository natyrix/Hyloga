import json
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import QuerySet, Avg
from django.db.models.expressions import RawSQL
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from AppointmentandBooking.models import Appointment, Booking
from Notification.models import Notification, ty
from Vendor.views import createNotification
from .validators import validate_image_size, validate_video_size
from Chat.models import Chat, sender
from Users.forms import CheckListForm, AccountForm, ImageForm, VideoForm, CategoryForm
from Vendor.models import Vendor, st, VendorImage, Pricing, Category
from accounts.models import AccountType, AcType
from .models import Users, CheckList, ImageGallery, VideoGallery, UsersImage, UsersVideo, Budget
from RateandReview.models import Rate, Review
from datetime import datetime
import threading


def setExpired(user):
    now = datetime.now()
    appts = Appointment.objects.filter(date__lt=now, user=user, expired=False, status=False, declined=False, canceled=False)
    bkgs = Booking.objects.filter(date__lt=now, user=user, expired=False, status=False, declined=False, canceled=False)
    chklists = CheckList.objects.filter(date_and_time__lt=now, user=user, is_passed=False, status=False)
    for ap in appts:
        ap.expired = True
        ap.save()
        createNotification(
            title="The appointment you have with vendor {} on date {} from {}-{} has been expired"
                .format(ap.vendor, ap.date, ap.start_time, ap.end_time),
            typ=ty[1][0],
            user=user,
            vendor=ap.vendor
        )
        createNotification(
            title="The appointment you have with {} on date {} from {}-{} has been expired"
                .format(ap.user, ap.date, ap.start_time, ap.end_time),
            typ=ty[2][0],
            user=user,
            vendor=ap.vendor
        )
    for bkg in bkgs:
        bkg.expired = True
        bkg.save()
        createNotification(
            title="The booking you have with vendor {} on date {} from {}-{} has been expired"
                .format(bkg.vendor, bkg.date, bkg.start_time, bkg.end_time),
            typ=ty[1][0],
            user=user,
            vendor=bkg.vendor
        )
        createNotification(
            title="The booking you have with {} on date {} from {}-{} has been expired"
                .format(bkg.user, bkg.date, bkg.start_time, bkg.end_time),
            typ=ty[2][0],
            user=user,
            vendor=bkg.vendor
        )
    for cl in chklists:
        cl.is_passed = True
        cl.save()
        createNotification(
            title="Your check list you have on {} at {}"
                .format(str(cl.date_and_time).split(' ')[0], str(cl.date_and_time).split(' ')[1]),
            typ=ty[1][0],
            user=user,
            vendor=None
        )


def getChatCount(users):
    chat_count = Chat.objects.filter(user=users, read_status=False, sender=sender[0][0])
    return chat_count.count()


def getChatCountWithVendor(user, vendor):
    chat_count = Chat.objects.filter(vendor=vendor, user=user, read_status=False, sender=sender[0][0])
    return chat_count.count()


def getNotificationCount(user):
    notification_count = Notification.objects.filter(user=user, type=ty[1][0], read_status=False)
    return notification_count.count()


def isUser(user):
    us = Users.objects.filter(login_id=user)
    if us:
        return True
    else:
        return False


def returnToHome(request, user):
    acType = AccountType.objects.get(user=request.user)
    if acType:
        if acType.Actype == AcType[1][0]:  # Vendor
            vendor = Vendor.objects.get(login_id=request.user)
            return redirect('vendor_dashboard', vendor.slug)
        elif acType.Actype == AcType[2][0]:  # Users
            users = Users.objects.get(login_id=request.user)
            return redirect('users_home', users.slug)
        else:
            return render(request, 'index.html')


def chckDate(date1, date2):
    if int(date1[0]) >= int(date2.year):
        if int(date1[0]) == int(date2.year):
            if int(date1[1]) >= int(date2.month):
                if int(date1[1]) == int(date2.month):
                    if int(date1[2]) > int(date2.day):
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        else:
            return True

    else:
        return False


def check_time(st_time, end_time):
    print(st_time)
    print(end_time)
    st_time = str(st_time).split(':')
    end_time = str(end_time).split(':')
    if int(st_time[0]) < int(end_time[0]):
        return True
    if int(st_time[0]) == int(end_time[0]):
        if int(st_time[1]) < int(end_time[1]):
            return True
    return False


def check_time2(st_time, end_time):
    st_time = str(st_time).split(':')
    end_time = str(end_time).split(':')
    if int(st_time[0]) < int(end_time[0]):
        return True
    if int(st_time[0]) == int(end_time[0]):
        if int(st_time[1]) <= int(end_time[1]):
            return True
    return False


def home(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if user.login_id == request.user:
                context = {
                    'users': user,
                    'not_count': getNotificationCount(user),
                    'chat_count': getChatCount(user)
                }
                return render(request, 'users/home.html', context)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')

    else:
        return HttpResponse("Page Not Found")


def users_search(request, id):
    if request.method == 'POST':
        search_txt = str(request.POST.get('search_txt', "Yelem")).strip()
        print(search_txt)
        return render(request, 'users/users_search.html')
    else:
        return render(request, 'index.html')


def users_vendors(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if user.login_id == request.user:
                category = request.GET.get('cat')
                rating = request.GET.get('rating')
                if category == 'all' or category is None:
                    category = None
                else:
                    category = str(category)
                    category = Category.objects.filter(category_name=category)
                    if category.exists():
                        category = category.first()
                    else:
                        category = None
                if category is None:
                    vendors = Vendor.objects.filter(status=st[0][0]).order_by('-id')
                else:
                    vendors = Vendor.objects.filter(status=st[0][0], category=category).order_by('-id')
                if rating == 'all' or rating is None:
                    rating = None
                else:
                    try:
                        rating = int(rating)
                        vendors = vendors.filter(id__in=RawSQL(
                            "SELECT vendor_id FROM RateandReview_rate "
                            "GROUP BY vendor_id HAVING AVG(rate_value) > {}".format(rating)
                            , []))
                    except ValueError:
                        rating = 'All'
                paginator = Paginator(vendors, 4)
                page = request.GET.get('page')
                paged_vendors = paginator.get_page(page)
                categories = Category.objects.filter(id__in=RawSQL(
                    "SELECT category_id FROM Vendor_vendor", []))
                ratings = []
                for vendor in paged_vendors:
                    vendor_rating = Rate.objects.filter(vendor=vendor).aggregate(Avg('rate_value'))
                    ratings.append(vendor_rating['rate_value__avg'])
                if category is None:
                    category = 'All'
                if rating is None:
                    rating = 'All'
                context = {
                    'users': user,
                    'vendors': paged_vendors,
                    'categories': categories,
                    'selected_cat': category,
                    'selected_rating': rating,
                    'ratings': ratings,
                    'not_count': getNotificationCount(user),
                    'chat_count': getChatCount(user)
                }
                return render(request, 'users/home.html', context)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def users_vendor(request, slug_txt):
    if request.user.is_authenticated:
        if isUser(request.user):
            vendor = Vendor.objects.filter(slug__iexact=slug_txt)
            if vendor.exists():
                vendor = vendor.first()
                users = Users.objects.get(login_id=request.user)
                vendor_images = VendorImage.objects.filter(vendor=vendor)
                vendor_ratings = Rate.objects.filter(vendor=vendor)
                vendor_pricing = Pricing.objects.filter(vendor=vendor)
                vendor_review = Review.objects.filter(vendor=vendor)
                user_can_review = vendor_review.filter(user=users)
                user_can_rate = vendor_ratings.filter(user=users)
                vendor_messages = Chat.objects.filter(vendor=vendor)
                vendor_appointments = Appointment.objects.filter(vendor=vendor, user=users).order_by('date')[:5]
                vendor_booking = Booking.objects.filter(vendor=vendor, user=users).order_by('date')[:5]
                context = {
                    'users': users,
                    'vendor': vendor,
                    'pricing': vendor_pricing,
                    'review': vendor_review,
                    'appointments': vendor_appointments,
                    'bookings': vendor_booking,
                    'not_count': getNotificationCount(users),
                    'chat_count': getChatCount(users)
                }
                if vendor_messages.exists():
                    user_messages = vendor_messages.filter(user=users).order_by('-id')
                    paginator = Paginator(user_messages, 4)
                    page = request.GET.get('page')
                    paged_messages = paginator.get_page(page)
                    context['vendor_messages'] = paged_messages
                if not user_can_rate.exists():
                    context['user_can_rate'] = True
                else:
                    user_rate = user_can_rate.first()
                    context['user_rate'] = user_rate
                if not user_can_review.exists():
                    context['user_can_review'] = True
                else:
                    user_review = user_can_review.first()
                    context['user_review'] = user_review
                if vendor_images.exists():
                    context['vendor_images'] = vendor_images
                if vendor_ratings.exists():
                    sum = 0
                    for rating in vendor_ratings:
                        sum += int(rating.rate_value)
                    avg = sum / vendor_ratings.count()
                    p_cal = 100 / vendor_ratings.count()
                    r5 = vendor_ratings.filter(rate_value='5')
                    if r5.exists():
                        r5_count = r5.count()
                        r5_p = p_cal * r5_count
                        context['r5_count'] = r5_count
                        context['r5_p'] = r5_p
                    r4 = vendor_ratings.filter(rate_value='4')
                    if r4.exists():
                        r4_count = r4.count()
                        r4_p = p_cal * r4_count
                        context['r4_count'] = r4_count
                        context['r4_p'] = r4_p
                    r3 = vendor_ratings.filter(rate_value='3')
                    if r3.exists():
                        r3_count = r3.count()
                        r3_p = p_cal * r3_count
                        context['r3_count'] = r3_count
                        context['r3_p'] = r3_p
                    r2 = vendor_ratings.filter(rate_value='2')
                    if r2.exists():
                        r2_count = r2.count()
                        r2_p = p_cal * r2_count
                        context['r2_count'] = r2_count
                        context['r2_p'] = r2_p
                    r1 = vendor_ratings.filter(rate_value='1')
                    if r1.exists():
                        r1_count = r1.count()
                        r1_p = p_cal * r1_count
                        context['r1_count'] = r1_count
                        context['r1_p'] = r1_p

                    context['vendor_ratings'] = vendor_ratings
                    context['r_avg'] = avg
                    context['r_count'] = vendor_ratings.count()
                wed_date = str(users.wedding_date).replace('-', '/')
                context['wed_date'] = wed_date
                return render(request, 'users/home.html', context)
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def rate_vendor(request, slug_txt):
    if request.user.is_authenticated:
        if isUser(request.user):
            if request.method == 'POST':
                vendor = Vendor.objects.filter(slug__iexact=slug_txt)
                if vendor.exists():
                    vendor = vendor.first()
                    users = Users.objects.get(login_id=request.user)
                    rate = request.POST['rate_val']
                    if 5 >= int(rate) >= 1:
                        ra = Rate(rate_value=rate, type="Vendor", vendor=vendor, user=users)
                        ra.save()
                        createNotification(
                            title="You have been rated with a {} star by {}".format(rate, users),
                            typ=ty[2][0],
                            user=users,
                            vendor=vendor
                        )
                        messages.success(request, "Rated successfully")
                        return redirect('users_vendor', vendor.slug)
                    else:
                        messages.error(request, "Rate value cannot exceed 5")
                        return redirect('users_vendor', vendor.slug)
                else:
                    return HttpResponse("Page Not Found")
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def appointments(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if user.login_id == request.user:
                ap = Appointment.objects.filter(user=user).order_by('-id')
                filt = request.GET.get('filter')
                if filt == 'All' or filt is None:
                    filt = None
                else:
                    filt = str(filt)
                    if filt == 'approved':
                        ap = ap.filter(status=True)
                    if filt == 'not_approved':
                        ap = ap.filter(status=False)
                    elif filt == 'declined':
                        ap = ap.filter(declined=True)
                    elif filt == 'expired':
                        ap = ap.filter(expired=True)
                paginator = Paginator(ap, 10)
                page = request.GET.get('page')
                p_ap = paginator.get_page(page)
                if filt is None:
                    filt = 'All'
                context = {
                    'users': user,
                    'appointments': p_ap,
                    'selected_filter': filt,
                    'not_count': getNotificationCount(user),
                    'chat_count': getChatCount(user)
                }
                return render(request, 'users/home.html', context)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def bookings(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if user.login_id == request.user:
                bk = Booking.objects.filter(user=user).order_by('-id')
                filt = request.GET.get('filter')
                if filt == 'All' or filt is None:
                    filt = None
                else:
                    filt = str(filt)
                    if filt == 'approved':
                        bk = bk.filter(status=True)
                    if filt == 'not_approved':
                        bk = bk.filter(status=False)
                    elif filt == 'declined':
                        bk = bk.filter(declined=True)
                    elif filt == 'expired':
                        bk = bk.filter(expired=True)
                paginator = Paginator(bk, 10)
                page = request.GET.get('page')
                p_bk = paginator.get_page(page)
                if filt is None:
                    filt = 'All'
                context = {
                    'users': user,
                    'bookings': p_bk,
                    'selected_filter': filt,
                    'not_count': getNotificationCount(user),
                    'chat_count': getChatCount(user)
                }
                return render(request, 'users/home.html', context)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def cancel_appointment(request, ap_id):
    if request.user.is_authenticated & isUser(request.user):
        user = Users.objects.get(login_id=request.user)
        appt = Appointment.objects.filter(user=user, canceled=False, id=ap_id)
        if appt.exists():
            appt = appt.first()
            appt.canceled = True
            appt.save()
            createNotification(
                title="The appointment you have with {} at {}, from {}-{} was canceled"
                    .format(user, appt.date, appt.start_time, appt.end_time),
                typ=ty[2][0],
                user=user,
                vendor=appt.vendor
            )
            messages.success(request, "Appointment canceled")
            return redirect('users_appointments', user.slug)
        else:
            messages.error(request, "Appointment cancel failed, the appointment you choose does not belong to you")
            return redirect('users_appointments', user.slug)
    return render(request, 'index.html')


def cancel_booking(request, bk_id):
    if request.user.is_authenticated & isUser(request.user):
        user = Users.objects.get(login_id=request.user)
        bk = Booking.objects.filter(user=user, canceled=False, id=bk_id)
        if bk.exists():
            bk = bk.first()
            bk.canceled = True
            bk.save()
            createNotification(
                title="The booking you have with {} at {}, from {}-{} was canceled"
                    .format(user, bk.date, bk.start_time, bk.end_time),
                typ=ty[2][0],
                user=user,
                vendor=bk.vendor
            )
            messages.success(request, "Booking canceled")
            return redirect('users_bookings', user.slug)
        else:
            messages.error(request, "Booking cancel failed, the booking you choose does not belong to you")
            return redirect('users_bookings', user.slug)
    return render(request, 'index.html')


def update_rate_vendor(request, rating_id):
    if request.user.is_authenticated:
        if isUser(request.user):
            if request.method == 'POST':
                rate = Rate.objects.filter(pk=rating_id)
                if rate.exists():
                    rate = rate.first()
                    vendor = rate.vendor
                    r_val = request.POST['update_rate_val']
                    if 5 >= int(r_val) >= 1:
                        rate.rate_value = r_val
                        rate.save()
                        createNotification(
                            title="Your rating by {} has been updated to {} star".format(rate.user, r_val),
                            typ=ty[2][0],
                            user=rate.user,
                            vendor=vendor
                        )
                        messages.success(request, "Rate updated successfully")
                        return redirect('users_vendor', vendor.slug)
                    else:
                        messages.error(request, "Invalid rate value")
                        return redirect('users_vendor', vendor.slug)
                else:
                    return HttpResponse("Page Not Found")
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def review_vendor(request, slug_txt):
    if request.user.is_authenticated:
        if isUser(request.user):
            if request.method == 'POST':
                vendor = Vendor.objects.filter(slug__iexact=slug_txt)
                if vendor.exists():
                    vendor = vendor.first()
                    users = Users.objects.get(login_id=request.user)
                    review = request.POST['review']
                    rev = Review(review=review, type="Vendor", vendor=vendor, user=users)
                    rev.save()
                    createNotification(
                        title="You have new review by {}".format(users),
                        typ=ty[2][0],
                        user=users,
                        vendor=vendor
                    )
                    messages.success(request, "Review submitted successfully")
                    return redirect('users_vendor', vendor.slug)
                else:
                    return HttpResponse("Page Not Found")
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def update_review_vendor(request, review_id):
    if request.user.is_authenticated:
        if isUser(request.user):
            if request.method == 'POST':
                review = Review.objects.filter(pk=review_id)
                if review.exists():
                    review = review.first()
                    vendor = review.vendor
                    rev_val = str(request.POST['updated_review']).strip()
                    review.review = rev_val
                    review.save()
                    createNotification(
                        title="Your review by {} has been updated".format(review.user),
                        typ=ty[2][0],
                        user=review.user,
                        vendor=vendor
                    )
                    messages.success(request, "Review updated successfully")
                    return redirect('users_vendor', vendor.slug)
                else:
                    return HttpResponse("Page Not Found")
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def send_message(request, slug_txt):
    if request.user.is_authenticated:
        if isUser(request.user):
            if request.method == 'POST':
                vendor = Vendor.objects.filter(slug__iexact=slug_txt)
                if vendor.exists():
                    vendor = vendor.first()
                    users = Users.objects.get(login_id=request.user)
                    msg_content = str(request.POST['msg']).strip()
                    cht = Chat(message=msg_content, user=users, vendor=vendor, sender=sender[1][0])
                    cht.save()
                    messages.success(request, "Message sent")
                    return redirect('users_vendor', vendor.slug)
                else:
                    return HttpResponse("Page Not Found")
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def users_chats(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if user.login_id == request.user:
                query = "SELECT * FROM `Chat_chat` WHERE id IN (SELECT MAX(id)" \
                        " FROM Chat_chat WHERE user_id = {} GROUP BY `vendor_id`) " \
                        "ORDER BY `id` DESC".format(user.id)
                user_chats = Chat.objects.raw(query)
                context = {
                    'users': user,
                    'not_count': getNotificationCount(user),
                }
                vendor_chat_count = []
                for u_chat in user_chats:
                    vendor_chat_count.append(getChatCountWithVendor(user, u_chat.vendor))
                if len(user_chats) > 0:
                    context['user_chats'] = user_chats
                    context['vendor_chat_counts'] = vendor_chat_count
                return render(request, 'users/home.html', context)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def markMsgUnread(chats):
    for chat in chats:
        if chat.sender == sender[0][0] and not chat.read_status:
            chat.read_status = True
            chat.save()


def user_vendor_chat(request, slug_txt):
    vendor = Vendor.objects.filter(slug__iexact=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                user = Users.objects.get(login_id=request.user)
                query = "SELECT * FROM `Chat_chat` WHERE id IN (SELECT MAX(id)" \
                        " FROM Chat_chat WHERE user_id = {} GROUP BY `vendor_id`) " \
                        "ORDER BY `id` DESC".format(user.id)
                user_chats = Chat.objects.raw(query)
                user_vendor_messages = Chat.objects.filter(vendor=vendor, user=user)
                markMsgUnread(user_vendor_messages)
                context = {
                    'users': user,
                    'ven': vendor,
                    'not_count': getNotificationCount(user)
                }
                vendor_chat_count = []
                for u_chat in user_chats:
                    vendor_chat_count.append(getChatCountWithVendor(user, u_chat.vendor))
                if len(user_chats) > 0:
                    context['user_chats'] = user_chats
                    context['vendor_chat_counts'] = vendor_chat_count
                if user_vendor_messages.exists():
                    context['user_vendor_chat'] = user_vendor_messages
                return render(request, 'users/home.html', context)
            else:
                returnToHome(request, request.user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def user_vendor_send_msg(request, slug_txt):
    if request.user.is_authenticated:
        if isUser(request.user):
            if request.method == 'POST':
                vendor = Vendor.objects.filter(slug__iexact=slug_txt)
                if vendor.exists():
                    vendor = vendor.first()
                    users = Users.objects.get(login_id=request.user)
                    msg_content = str(request.POST['msg']).strip()
                    cht = Chat(message=msg_content, user=users, vendor=vendor, sender=sender[1][0])
                    cht.save()
                    return redirect('user_vendor_chat', vendor.slug)
                else:
                    return HttpResponse("Page Not Found")
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def check_list(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                if request.user == user.login_id:
                    if request.method == 'POST':
                        check_list_form = CheckListForm(request.POST)
                        c_date = request.POST['_list_date_time']
                        ch_date_time = str(c_date).strip().split('T')
                        ch_date = ch_date_time[0].split('-')
                        if check_list_form.is_valid():
                            order_num = int(check_list_form.cleaned_data['order_number'])
                            if 0 < order_num <= 50:
                                curDate = datetime.now()
                                endDate = user.wedding_date
                                if chckDate(ch_date, curDate) and not chckDate(ch_date, endDate):
                                    c_date = c_date.replace('T', ' ')
                                    c_date = timezone.make_aware(datetime.strptime(c_date, '%Y-%m-%d %H:%M'))
                                    content = check_list_form.cleaned_data['content']
                                    checkList = CheckList(
                                        order_number=order_num,
                                        content=content,
                                        user=user,
                                        date_and_time=c_date
                                    )
                                    checkList.save()
                                    messages.success(request, "Check-list added successfully")
                                    return redirect('users_check_list', user.slug)
                                else:
                                    if not chckDate(ch_date, curDate):
                                        messages.error(request, "Date can not be set to a past date")
                                        return redirect('users_check_list', user.slug)
                                    else:
                                        messages.error(request, "Date can not be set after your wedding date")
                                        return redirect('users_check_list', user.slug)
                            else:
                                messages.error(request, "Order number must be between 1 and 50")
                                return redirect('users_check_list', user.slug)
                        else:
                            messages.error(request, "Invalid data provided")
                            return redirect('users_check_list', user.slug)
                    else:
                        check_lists = CheckList.objects.filter(user=user).order_by('order_number')
                        paginator = Paginator(check_lists, 10)
                        page = request.GET.get('page')
                        paged_check_lists = paginator.get_page(page)
                        context = {
                            'users': user,
                            'check_list_form': CheckListForm,
                            'not_count': getNotificationCount(user),
                            'chat_count': getChatCount(user)
                        }
                        if check_lists.exists():
                            context['check_lists'] = paged_check_lists
                        return render(request, 'users/home.html', context)
                else:
                    return returnToHome(request, user)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def users_account(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                if request.user == user.login_id:

                    account_form = AccountForm(instance=user)
                    context = {
                        'users': user,
                        'account_form': account_form,
                        'not_count': getNotificationCount(user),
                        'chat_count': getChatCount(user)
                    }
                    return render(request, 'users/home.html', context)
                else:
                    return returnToHome(request, user)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def users_edit_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if isUser(request.user):
                user = Users.objects.get(login_id=request.user)
                account_form = AccountForm(request.POST)
                if account_form.is_valid():
                    wed_date = request.POST['wed_date']
                    strWedDate = str(wed_date).split('-')
                    today = datetime.today()
                    if chckDate(strWedDate, today):
                        user.first_name = account_form.cleaned_data['first_name']
                        user.last_name = account_form.cleaned_data['last_name']
                        user.email = account_form.cleaned_data['email']
                        user.role = account_form.cleaned_data['role']
                        user.fiance_first_name = account_form.cleaned_data['fiance_first_name']
                        user.fiance_last_name = account_form.cleaned_data['fiance_last_name']
                        user.fiance_email = account_form.cleaned_data['fiance_email']
                        user.wedding_date = wed_date
                        user.save()
                        users = User.objects.get(pk=user.login_id.id)
                        users.email = account_form.cleaned_data['email']
                        email = account_form.cleaned_data['email']
                        uname = email.split('@')
                        users.username = uname[0]
                        users.save()
                        messages.success(request, "Profile updated successfully")
                        return redirect('users_account', user.slug)
                    else:
                        messages.error(request, "Wedding date can not be set to past date")
                        return redirect('users_account', user.slug)
                else:
                    messages.error(request, "Profile edit failed")
                    return redirect('users_account', user.slug)
            else:
                returnToHome(request, request.user)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def users_edit_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if isUser(request.user):
                old_password = str(request.POST['old_password']).strip()
                password = str(request.POST['password']).strip()
                password2 = str(request.POST['password2']).strip()
                users = Users.objects.get(login_id=request.user)
                user = User.objects.get(pk=users.login_id.id)
                user1 = auth.authenticate(username=user.username, password=old_password)
                if user1 is not None:
                    if password == password2:
                        if password != old_password:
                            user.set_password(password)
                            user.save()
                            messages.success(request, "Password changed successfully")
                            return redirect('login')
                        else:
                            messages.error(request, "New password is the same as old password")
                            return redirect('users_account', users.slug)
                    else:
                        messages.error(request, "Passwords do not match")
                        return redirect('users_account', users.slug)
                else:
                    messages.error(request, "Old password is not correct")
                    return redirect('users_account', users.slug)
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def gallery(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                user_images = ImageGallery.objects.filter(user=user).order_by('-id')
                user_videos = VideoGallery.objects.filter(user=user).order_by('-id')
                context = {
                    'users': user,
                    'user_images': user_images,
                    'user_videos': user_videos,
                    'not_count': getNotificationCount(user),
                    'chat_count': getChatCount(user)
                }
                return render(request, 'users/home.html', context)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def upload(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                context = {
                    'users': user,
                    'image_form': ImageForm,
                    'video_form': VideoForm,
                    'not_count': getNotificationCount(user),
                    'chat_count': getChatCount(user)
                }
                return render(request, 'users/home.html', context)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def delete_image(request, img_id):
    if request.user.is_authenticated:
        if isUser(request.user):
            user = Users.objects.get(login_id=request.user)
            img = ImageGallery.objects.filter(pk=img_id)
            if img.exists():
                img = img.first()
                if user == img.user:
                    img.delete()
                    messages.warning(request, "Image deleted")
                    return redirect('users_gallery', user.slug)
                else:
                    messages.error(request, "Access Denied")
                    return redirect('users_gallery', user.slug)
            else:
                messages.error(request, 'Image not found')
                return redirect('users_gallery', user.slug)
        else:
            returnToHome(request, request.user)
    else:
        return render(request, 'index.html')


def delete_vid(request, vid_id):
    if request.user.is_authenticated:
        if isUser(request.user):
            user = Users.objects.get(login_id=request.user)
            vid = VideoGallery.objects.filter(pk=vid_id)
            if vid.exists():
                vid = vid.first()
                if user == vid.user:
                    vid.delete()
                    messages.warning(request, "Video deleted")
                    return redirect('users_gallery', user.slug)
                else:
                    messages.error(request, "Access Denied")
                    return redirect('users_gallery', user.slug)
            else:
                messages.error(request, 'Video not found')
                return redirect('users_gallery', user.slug)
        else:
            returnToHome(request, request.user)
    else:
        return render(request, 'index.html')


def upload_image(request, slug_txt):
    if request.method == 'POST':
        users = Users.objects.filter(slug__iexact=slug_txt)
        if users.exists():
            users = users.first()
            if request.user.is_authenticated:
                if isUser(request.user):
                    if request.user == users.login_id:
                        image_form = ImageForm(request.POST, request.FILES)
                        if image_form.is_valid():
                            if validate_image_size(request.FILES['image_location']):
                                user_img = UsersImage(user=users, image_location=request.FILES['image_location'])
                                user_img.save()
                                messages.success(request, "Image uploaded successfully, and will be added to your"
                                                          " gallery soon.")
                                return redirect('users_upload', users.slug)
                            else:
                                messages.error(request, "Image size can not exceed 10MB.")
                                return redirect('users_upload', users.slug)
                        else:
                            messages.error(request, "Upload Failed size can not exceed 10MB")
                            return redirect('users_upload', users.slug)
                    else:
                        return redirect('users_home', users.slug)
                else:
                    returnToHome(request, users)
            else:
                return render(request, 'index.html')
        else:
            return HttpResponse("Page Not Found")


def upload_video(request, slug_txt):
    if request.method == 'POST':
        users = Users.objects.filter(slug__iexact=slug_txt)
        if users.exists():
            users = users.first()
            if request.user.is_authenticated:
                if isUser(request.user):
                    if request.user == users.login_id:
                        vid_form = VideoForm(request.POST, request.FILES)
                        if vid_form.is_valid():
                            if validate_video_size(request.FILES['video_location']):
                                user_vid = UsersVideo(user=users, video_location=request.FILES['video_location'])
                                user_vid.save()
                                messages.success(request, "Video uploaded successfully, and will be added to your"
                                                          " gallery soon.")
                                return redirect('users_upload', users.slug)
                            else:
                                messages.error(request, "Video size can not exceed 30MB")
                                return redirect('users_upload', users.slug)

                        else:
                            messages.error(request, "Upload Failed")
                            return redirect('users_upload', users.slug)
                    else:
                        return redirect('users_home', users.slug)
                else:
                    returnToHome(request, users)
            else:
                return render(request, 'index.html')
        else:
            return HttpResponse("Page Not Found")


def edit_check_list(request, slug_txt):
    if request.method == 'POST':
        user = Users.objects.filter(slug__iexact=slug_txt)
        if user.exists():
            user = user.first()
            if request.user.is_authenticated:
                if isUser(request.user):
                    cl_id = request.POST['ch_id']
                    check_list = CheckList.objects.filter(pk=cl_id)
                    if check_list.exists():
                        check_list = check_list.first()
                        if request.user == user.login_id and request.user == check_list.user.login_id:
                            order_num = str(request.POST['ed_order_number']).strip()
                            content = str(request.POST['ed_content']).strip()
                            st = False
                            if 'edstatus' in request.POST:
                                st = True
                            c_date = request.POST['eddatetime']
                            ch_date_time = str(c_date).strip().split('T')
                            ch_date = ch_date_time[0].split('-')
                            if 0 < int(order_num) <= 50:
                                curDate = datetime.now()
                                endDate = user.wedding_date
                                if chckDate(ch_date, curDate) and not chckDate(ch_date, endDate):
                                    c_date = c_date.replace('T', ' ')
                                    c_date = timezone.make_aware(datetime.strptime(c_date, '%Y-%m-%d %H:%M'))
                                    check_list.order_number = order_num
                                    check_list.date_and_time = c_date
                                    check_list.status = st
                                    check_list.content = content
                                    check_list.save()
                                    messages.success(request, "Check-list updated successfully")
                                    return redirect('users_check_list', user.slug)
                                else:
                                    if not chckDate(ch_date, curDate):
                                        messages.error(request, "Date can not be set to a past date")
                                        return redirect('users_check_list', user.slug)
                                    else:
                                        messages.error(request, "Date can not be set after your wedding date")
                                        return redirect('users_check_list', user.slug)
                            else:
                                messages.error(request, "Order number must be between 1 and 50")
                                return redirect('users_check_list', user.slug)
                        else:
                            messages.error(request, "Access denied")
                            return redirect('users_check_list', user.slug)
                    else:
                        return HttpResponse("Page Not Found")
                else:
                    return returnToHome(request, user)
            else:
                return render(request, 'index.html')
        else:
            return HttpResponse("Page Not Found")
    else:
        return HttpResponse("Page Not Found")


def removeDuplicate(cobnLists):
    for ls in cobnLists:
        ls.sort()
    for i, ls in enumerate(cobnLists, start=1):
        for j in range(i, len(cobnLists)):
            if ls == cobnLists[j]:
                cobnLists[j] = ''
    ncobnLists = []
    for ls in cobnLists:
        if ls != '':
            ncobnLists.append(ls)
    return ncobnLists


def createPriceList(cobnLists, x):
    index = sorted(range(len(cobnLists)), key=lambda i: len(cobnLists[i]), reverse=True)[:x]
    cl = []
    for i in index:
        cl.append(cobnLists[i])
    cobnLists = cl
    plist = []
    pricings = Pricing.objects.all()
    for priceList in cobnLists:
        p = []
        for price in priceList:
            p.append(pricings.get(id=int(price.split(':')[0])))
        plist.append(p)
    return plist


def calcBudget(amount, categories, sort_choice='best_of_3'):
    amount = int(amount) + 1
    prlist = []
    cobnLists = []
    for category in categories:
        vendors = Vendor.objects.filter(category_id=int(category))
        for vendor in vendors:
            vprs = Pricing.objects.filter(vendor=vendor)
            if vprs.exists():
                for vpr in vprs:
                    if vpr.value <= amount:
                        pr = "{}:{}:{}:{}".format(vpr.id, int(vpr.value), vendor.id, vendor.category.id)
                        prlist.append(pr)
    for price in prlist:
        s1 = price.split(':')
        pr1 = int(s1[1])
        vid1 = s1[2]
        vcat1 = s1[3]
        amt = amount - pr1
        ls = [price]
        for i, prc in enumerate(prlist):
            s2 = prc.split(':')
            pr2 = int(s2[1])
            vid2 = s2[2]
            vcat2 = s2[3]
            vid3 = ''
            vcat3 = ''
            if (i + 1) < len(prlist):
                s3 = prlist[i + 1].split(':')
                vid3 = s3[2]
                vcat3 = s3[3]
            if vid1 != vid2 and vcat1 != vcat2 and vcat2 != vcat3 and vid2 != vid3:
                if pr2 < amt:
                    amt = amt - pr2
                    ls.append(prc)
        cobnLists.append(ls)
    cobnLists = removeDuplicate(cobnLists)
    if sort_choice == 'best_of_3':
        if len(cobnLists) > 3:
            return createPriceList(cobnLists, 3)
        else:
            return createPriceList(cobnLists, len(cobnLists))
    elif sort_choice == 'best_of_5':
        if len(cobnLists) > 5:
            return createPriceList(cobnLists, 5)
        else:
            return createPriceList(cobnLists, len(cobnLists))
    elif sort_choice == 'best_1':
        if len(cobnLists) > 1:
            return createPriceList(cobnLists, 1)
        else:
            return createPriceList(cobnLists, len(cobnLists))
    else:
        return createPriceList(cobnLists, 10)


def budget(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                if request.user == user.login_id:
                    context = {
                        'users': user,
                        'budget_form': CategoryForm(),
                        'not_count': getNotificationCount(user),
                        'chat_count': getChatCount(user)
                    }
                    if request.method == 'POST':
                        budget_form = CategoryForm(request.POST)
                        if budget_form.is_valid():
                            svcs = budget_form.cleaned_data['vendor_categories']
                            cats = []
                            for cat in svcs:
                                cats.append(cat.id)

                            amount = budget_form.cleaned_data['amount']
                            sort_choice = budget_form.cleaned_data['sort']
                            price_lists = calcBudget(amount, cats, str(sort_choice))
                            context['price_lists'] = price_lists
                            context['amount'] = amount
                            if len(price_lists) > 0:
                                messages.success(request, "Budget plan generated successfully")
                                return render(request, 'users/home.html', context)
                            messages.warning(request, "Budget plan can not be generated for your combination")
                            return render(request, 'users/home.html', context)
                        else:
                            messages.error(request, "Something went wrong please try again")
                            return render(request, 'users/home.html', context)
                    else:
                        return render(request, 'users/home.html', context)
                else:
                    return redirect('users_home', user.slug)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def save_budget(request, slug_txt):
    if request.is_ajax and request.method == 'POST':
        user = Users.objects.filter(slug__iexact=slug_txt)
        if user.exists():
            user = user.first()
            if request.user.is_authenticated:
                if isUser(request.user):
                    if request.user == user.login_id:
                        price_lists = request.POST.get('budget_prices')
                        amount = request.POST.get('budget_amount')
                        if amount is not None and price_lists is not None:
                            price_lists = str(price_lists)[:-1].strip()
                            amount = float(str(amount).strip())
                            budget_plans = Budget.objects.filter(user=user)
                            x = 0
                            if budget_plans.exists():
                                budget_plans = budget_plans.filter(prices__iexact=price_lists)
                                if budget_plans.exists():
                                    budget_plans = budget_plans.filter(amount=amount)
                                    if budget_plans.exists():
                                        x = 1
                            if x == 0:
                                budget_plan = Budget(
                                    user=user,
                                    amount=amount,
                                    prices=price_lists
                                )
                                budget_plan.save()
                                # budget_plan_ser = serializers.serialize('json', [budget_plan, ])
                                return JsonResponse({'message': "Plan successfully saved"}, status=200)
                            else:
                                return JsonResponse({'error': "This plan already exists"}, status=422)
                    else:
                        return redirect('users_home', user.slug)
                else:
                    return returnToHome(request, user)
            else:
                return render(request, 'index.html')
        else:
            return HttpResponse("Page Not Found")


def get_all_budget(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                if request.user == user.login_id:
                    context = {
                        'users': user,
                        'not_count': getNotificationCount(user),
                        'chat_count': getChatCount(user)
                    }
                    users_budget = Budget.objects.filter(user=user).order_by('-id').order_by('-amount')
                    if users_budget.exists():
                        paginator = Paginator(users_budget, 2)
                        page = request.GET.get('page')
                        users_budgets = paginator.get_page(page)
                        bud_list = []
                        for u_b in users_budgets:
                            pl = [u_b.amount, ]
                            plist = str(u_b.prices).split(',')
                            for p in plist:
                                pr_obj = Pricing.objects.filter(pk=int(p))
                                if pr_obj.exists():
                                    pr_obj = pr_obj.first()
                                    pl.append(pr_obj)
                            bud_list.append(pl)
                        context['users_budgets'] = users_budgets
                        context['budget_list'] = bud_list
                        return render(request, 'users/home.html', context)
                    else:
                        return render(request, 'users/home.html', context)
                else:
                    return redirect('users_home', user.slug)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def make_appointment(request, slug_txt):
    if request.is_ajax and request.method == 'POST':
        user = Users.objects.filter(slug__iexact=slug_txt)
        if user.exists():
            user = user.first()
            if request.user.is_authenticated:
                if isUser(request.user):
                    if request.user == user.login_id:
                        app_date = request.POST.get('ap_date')
                        app_end_time = request.POST.get('ap_en_time')
                        app_st_time = request.POST.get('ap_st_time')
                        app_vendor = request.POST.get('ap_vendor_id')
                        if app_date is not None and app_end_time is not None and app_st_time is not None and app_vendor is not None:
                            dat = datetime.now()
                            wed_date = user.wedding_date
                            if chckDate(app_date.split('-'), dat) and not chckDate(app_date.split('-'), wed_date):
                                app_vendor = int(app_vendor)
                                vendor = Vendor.objects.filter(pk=app_vendor)
                                if vendor.exists():
                                    vendor = vendor.first()
                                    if check_time(app_st_time, app_end_time):
                                        x = 0
                                        appointments = Appointment.objects.filter(vendor=vendor, status=True)
                                        if appointments.exists():
                                            appointments = appointments.filter(date=app_date)
                                            if appointments.exists():
                                                for appointment in appointments:
                                                    if appointment.status:
                                                        en_time = appointment.end_time
                                                        if not check_time2(en_time, app_st_time):
                                                            x = 1
                                        if x == 0:
                                            appt = Appointment(
                                                date=app_date,
                                                start_time=app_st_time,
                                                end_time=app_end_time,
                                                user=user,
                                                vendor=vendor
                                            )
                                            appt.save()
                                            createNotification(
                                                title="You have new appointment request with {} at {} from {}-{}"
                                                    .format(user, appt.date, appt.start_time, appt.end_time),
                                                typ=ty[2][0],
                                                user=user,
                                                vendor=vendor
                                            )
                                            return JsonResponse({'message': "Appointment request successful, please "
                                                                            "wait "
                                                                            "for the vendor's approval"}, status=200)
                                        else:
                                            return JsonResponse(
                                                {
                                                    'error': "Vendor has another appointment on the provided date and "
                                                             "time"},
                                                status=422)
                                    else:
                                        return JsonResponse(
                                            {
                                                'error': "End time can not be set earlier to start time, Appointment "
                                                         "can not "
                                                         "be set"},
                                            status=422)
                                else:
                                    return JsonResponse({'error': "Vendor does not exist, Appointment can not be set"},
                                                        status=422)
                            else:
                                if not chckDate(app_date.split('-'), dat):
                                    return JsonResponse({'error': "Appointment date can not be set to a past date, "
                                                                  "Appointment can not be set"}, status=422)
                                else:
                                    return JsonResponse({'error': "Appointment date can not be set after your wedding "
                                                                  "date, "
                                                                  "Appointment can not be set"}, status=422)
                        else:
                            return JsonResponse({'error': "Invalid data provided, Appointment can not be set"},
                                                status=422)
                    else:
                        return redirect('users_home', user.slug)
                else:
                    return returnToHome(request, user)
            else:
                return render(request, 'index.html')
        else:
            return HttpResponse("Page Not Found")


def make_booking(request, slug_txt):
    if request.is_ajax and request.method == 'POST':
        user = Users.objects.filter(slug__iexact=slug_txt)
        if user.exists():
            user = user.first()
            if request.user.is_authenticated:
                if isUser(request.user):
                    if request.user == user.login_id:
                        book_date = request.POST.get('bk_date')
                        book_end_time = request.POST.get('bk_en_time')
                        book_start_time = request.POST.get('bk_st_time')
                        book_vendor = request.POST.get('bk_vendor_id')
                        if book_date is not None and book_end_time is not None and book_start_time is not None and book_vendor is not None:
                            dat = datetime.now()
                            wed_date = user.wedding_date
                            if chckDate(book_date.split('-'), dat) and not chckDate(book_date.split('-'), wed_date):
                                book_vendor = int(book_vendor)
                                vendor = Vendor.objects.filter(pk=book_vendor)
                                if vendor.exists():
                                    vendor = vendor.first()
                                    if check_time(book_start_time, book_end_time):
                                        x = 0
                                        bookings = Booking.objects.filter(vendor=vendor, status=True)
                                        if bookings.exists():
                                            bookings = bookings.filter(date=book_date)
                                            if bookings.exists():
                                                for booking in bookings:
                                                    if booking.status:
                                                        en_time = booking.end_time
                                                        if not check_time2(en_time, book_start_time):
                                                            x = 1
                                        if x == 0:
                                            bkg = Booking(
                                                date=book_date,
                                                start_time=book_start_time,
                                                end_time=book_end_time,
                                                user=user,
                                                vendor=vendor
                                            )
                                            bkg.save()
                                            createNotification(
                                                title="You have new booking request with {} at {} from {}-{}"
                                                    .format(user, bkg.date, bkg.start_time, bkg.end_time),
                                                typ=ty[2][0],
                                                user=user,
                                                vendor=vendor
                                            )
                                            return JsonResponse({'message': "Booking request successful, please "
                                                                            "wait "
                                                                            "for the vendor's approval"}, status=200)
                                        else:
                                            return JsonResponse(
                                                {
                                                    'error': "Vendor has another booking on the provided date and "
                                                             "time"},
                                                status=422)
                                    else:
                                        return JsonResponse(
                                            {
                                                'error': "End time can not be set earlier to start time, Booking can "
                                                         "not "
                                                         "be set"},
                                            status=422)
                                else:
                                    return JsonResponse({'error': "Vendor does not exist, Booking can not be set"},
                                                        status=422)
                            else:
                                if not chckDate(book_date.split('-'), dat):
                                    return JsonResponse({'error': "Booking date can not be set to a past date, "
                                                                  "Booking can not be set"}, status=422)
                                else:
                                    return JsonResponse({'error': "Booking date can not be set after your wedding "
                                                                  "date, "
                                                                  "Booking can not be set"}, status=422)
                        else:
                            return JsonResponse({'error': "Invalid data provided, Booking can not be set"}, status=422)
                    else:
                        return redirect('users_home', user.slug)
                else:
                    return returnToHome(request, user)
            else:
                return render(request, 'index.html')
        else:
            return HttpResponse("Page Not Found")


def makeUnread(user):
    notir = Notification.objects.filter(user=user, type=ty[1][0], read_status=False).order_by('-id')
    for n in notir:
        if not n.read_status:
            n.read_status = True
            n.save()


def notification(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if isUser(request.user):
                if request.user == user.login_id:
                    notif = Notification.objects.filter(user=user, type=ty[1][0]).order_by('-id')
                    paginator = Paginator(notif, 10)
                    page = request.GET.get('page')
                    paged_not = paginator.get_page(page)
                    context = {
                        'users': user,
                        'chat_count': getChatCount(user)
                    }
                    st = threading.Timer(5, makeUnread, (user,))
                    st.start()
                    # makeUnread(user)
                    if notif.exists():
                        context['notifications'] = paged_not
                    return render(request, 'users/home.html', context)
                else:
                    return redirect('users_home', user.slug)
            else:
                return returnToHome(request, user)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")
