import threading

from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import RateandReview
from AppointmentandBooking.models import Appointment, Booking
from Chat.models import Chat, sender
from Notification.models import Notification, ty
from RateandReview.models import Rate, Review
from Users.models import Users
from accounts.models import AccountType, AcType
from .models import Vendor, Pricing, VendorImage
from .form import PricingForm, GalleryForm, LogoForm, AccountForm
from datetime import datetime


def setExpiredVendor(vendor):
    now = datetime.now()
    appts = Appointment.objects.filter(date__lt=now, vendor=vendor, expired=False, status=False, declined=False,
                                       canceled=False)
    bkgs = Booking.objects.filter(date__lt=now, vendor=vendor, expired=False, status=False, declined=False,
                                  canceled=False)
    for ap in appts:
        ap.expired = True
        ap.save()
        createNotification(
            title="The appointment you have with vendor {} on date {} from {}-{} has been expired"
                .format(ap.vendor, ap.date, ap.start_time, ap.end_time),
            typ=ty[1][0],
            user=ap.user,
            vendor=vendor
        )
        createNotification(
            title="The appointment you have with {} on date {} from {}-{} has been expired"
                .format(ap.user, ap.date, ap.start_time, ap.end_time),
            typ=ty[2][0],
            user=ap.user,
            vendor=vendor
        )
    for bkg in bkgs:
        bkg.expired = True
        bkg.save()
        createNotification(
            title="The booking you have with vendor {} on date {} from {}-{} has been expired"
                .format(bkg.vendor, bkg.date, bkg.start_time, bkg.end_time),
            typ=ty[1][0],
            user=bkg.user,
            vendor=vendor
        )
        createNotification(
            title="The booking you have with {} on date {} from {}-{} has been expired"
                .format(bkg.user, bkg.date, bkg.start_time, bkg.end_time),
            typ=ty[2][0],
            user=bkg.user,
            vendor=vendor
        )


def createNotification(title, typ, user, vendor):
    notification = Notification(
        title=title,
        type=typ,
        user=user,
        vendor=vendor
    )
    notification.save()


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


def getNotificationCount(vendor):
    notification_count = Notification.objects.filter(vendor=vendor, type=ty[2][0], read_status=False)
    return notification_count.count()


def getChatCount(vendor):
    chat_count = Chat.objects.filter(vendor=vendor, read_status=False, sender=sender[1][0])
    return chat_count.count()


def getChatCountWithUser(vendor, user):
    chat_count = Chat.objects.filter(vendor=vendor, user=user, read_status=False, sender=sender[1][0])
    return chat_count.count()


def isVendor(user):
    vendor = Vendor.objects.filter(login_id=user)
    if vendor:
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


def dashboard(request, slug_txt):
    vendor = Vendor.objects.filter(slug__iexact=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated:
            if vendor.login_id == request.user:
                context = {
                    'vendor': vendor,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                return returnToHome(request, vendor)

        else:
            return render(request, 'index.html')

    else:
        return HttpResponse("Page Not Found")


def pricing(request, slug_txt):
    vendor = Vendor.objects.filter(slug__iexact=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated:
            if vendor.login_id == request.user:
                pricings = Pricing.objects.filter(vendor=vendor).order_by('-id')
                context = {
                    'vendor': vendor,
                    'pricings': pricings,
                    'pricing_form': PricingForm,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                return returnToHome(request, vendor)

        else:
            return render(request, 'index.html')

    else:
        return HttpResponse("Page Not Found")


def edit_pricing(request, price_id):
    if request.method == "POST":
        if request.user.is_authenticated & isVendor(request.user):
            vendor = Vendor.objects.get(login_id=request.user)
            pricing = Pricing.objects.get(pk=price_id)
            if vendor == pricing.vendor:
                form = PricingForm(request.POST)
                if form.is_valid():
                    title = form.cleaned_data['title']
                    value = form.cleaned_data['value']
                    detail = form.cleaned_data['detail']
                    pricing.title = title
                    pricing.value = value
                    pricing.detail = detail
                    pricing.save()
                    messages.success(request, "Pricing edited successfully")
                    return redirect('vendor_pricing', vendor.slug)
                else:
                    return redirect('vendor_pricing', vendor.slug)
            else:
                return redirect('vendor_pricing', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        pricing = get_object_or_404(Pricing, pk=price_id)
        vendor = pricing.vendor
        form = PricingForm(instance=pricing)
        context = {
            'pricing': pricing,
            'vendor': vendor,
            'pricing_form': form,
            'chat_count': getChatCount(vendor),
            'not_count': getNotificationCount(vendor),
        }
        return render(request, 'vendor/edit_pricing.html', context)


def add_pricing(request):
    if request.method == 'POST':
        if request.user.is_authenticated & isVendor(request.user):
            vendor = Vendor.objects.get(login_id=request.user)
            pricing_form = PricingForm(request.POST)
            if pricing_form.is_valid():
                title = pricing_form.cleaned_data['title']
                detail = pricing_form.cleaned_data['detail']
                value = pricing_form.cleaned_data['value']
                pricing1 = Pricing(title=title, detail=detail, value=value, vendor=vendor)
                pricing1.save()
                messages.success(request, "Price added successfully")
                return redirect('vendor_pricing', vendor.slug)
            else:
                messages.error(request, "Price cannot be added")
                return redirect('vendor_pricing', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def delete_pricing(request, price_id):
    if request.method == 'POST':
        if request.user.is_authenticated & isVendor(request.user):
            vendor = Vendor.objects.get(login_id=request.user)
            pricing = Pricing.objects.get(pk=price_id)
            if vendor == pricing.vendor:
                pricing.delete()
                messages.warning(request, "Pricing deleted")
                return redirect('vendor_pricing', vendor.slug)
            else:
                return redirect('vendor_pricing', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def gallery(request, slug_txt):
    vendor = Vendor.objects.filter(slug__iexact=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated:
            if vendor.login_id == request.user:
                vendor_images = VendorImage.objects.filter(vendor=vendor).order_by('-id')
                context = {
                    'vendor': vendor,
                    'vendor_images': vendor_images,
                    'gallery_form': GalleryForm,
                    'logo_form': LogoForm,
                    'logo': vendor.logo,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                return returnToHome(request, vendor)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def update_logo(request):
    if request.method == 'POST':
        if request.user.is_authenticated & isVendor(request.user):
            vendor = Vendor.objects.get(login_id=request.user)
            logo_form = LogoForm(request.POST, request.FILES)
            if logo_form.is_valid():
                vendor.logo = request.FILES['logo']
                vendor.save()
                messages.success(request, 'Logo updated successfully')
                return redirect('vendor_gallery', vendor.slug)
            else:
                messages.error(request, 'Logo updated failed')
                return redirect('vendor_gallery', vendor.slug)
    else:
        return render(request, 'index.html')


def add_image(request):
    if request.method == 'POST':
        if request.user.is_authenticated & isVendor(request.user):
            vendor = Vendor.objects.get(login_id=request.user)
            image_form = GalleryForm(request.POST, request.FILES)
            if image_form.is_valid():
                vendorImage = VendorImage(vendor=vendor, image_location=request.FILES['image_location'])
                vendorImage.save()
                messages.success(request, "Image added successfully")
                return redirect('vendor_gallery', vendor.slug)
            else:
                messages.error(request, "Upload Failed")
                return redirect('vendor_gallery', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def delete_image(request, img_id):
    if request.user.is_authenticated & isVendor(request.user):
        vendor = Vendor.objects.get(login_id=request.user)
        img = VendorImage.objects.filter(pk=img_id)
        if img.exists():
            img = img.first()
            if vendor == img.vendor:
                img.delete()
                messages.warning(request, "Image deleted")
                return redirect('vendor_gallery', vendor.slug)
            else:
                messages.error(request, "Access Denied")
                return redirect('vendor_gallery', vendor.slug)
        else:
            messages.warning(request, "Image not found")
            return redirect('vendor_gallery', vendor.slug)

    else:
        return render(request, 'index.html')


def account(request, slug_txt):
    vendor = Vendor.objects.filter(slug=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated & isVendor(request.user):
            if vendor.login_id == request.user:
                account_form = AccountForm(instance=vendor)
                context = {
                    'vendor': vendor,
                    'account_form': account_form,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def edit_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated & isVendor(request.user):
            vendor = Vendor.objects.get(login_id=request.user)
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                vendor.email = account_form.cleaned_data['email']
                vendor.name = account_form.cleaned_data['name']
                vendor.phonenumber = account_form.cleaned_data['phonenumber']
                vendor.address = account_form.cleaned_data['address']
                vendor.category = account_form.cleaned_data['category']
                vendor.save()
                user = User.objects.get(pk=vendor.login_id.id)
                user.email = account_form.cleaned_data['email']
                email = account_form.cleaned_data['email']
                uname = email.split('@')
                user.username = uname[0]
                user.save()
                messages.success(request, "Profile edit successfully")
                return redirect('vendor_account', vendor.slug)
            else:
                messages.error(request, "Profile edit failed")
                return redirect('vendor_account', vendor.slug)

        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def edit_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if isVendor(request.user):
                old_password = str(request.POST['old_password']).strip()
                password = str(request.POST['password']).strip()
                password2 = str(request.POST['password2']).strip()
                vendor = Vendor.objects.get(login_id=request.user)
                user = User.objects.get(pk=vendor.login_id.id)
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
                            return redirect('vendor_account', vendor.slug)
                    else:
                        messages.error(request, "Passwords do not match")
                        return redirect('vendor_account', vendor.slug)
                else:
                    messages.error(request, "Old password is not correct")
                    return redirect('vendor_account', vendor.slug)
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def ratings(request, slug_txt):
    vendor = Vendor.objects.filter(slug=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated & isVendor(request.user):
            if vendor.login_id == request.user:
                vendor_ratings = Rate.objects.filter(vendor=vendor).order_by('-id')
                paginator = Paginator(vendor_ratings, 12)
                page = request.GET.get('page')
                paged_rating = paginator.get_page(page)
                context = {
                    'vendor': vendor,
                    'ratings': paged_rating,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
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
                    context['r_avg'] = avg
                    context['r_count'] = vendor_ratings.count()
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def reviews(request, slug_txt):
    vendor = Vendor.objects.filter(slug=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated & isVendor(request.user):
            if vendor.login_id == request.user:
                vendor_reviews = Review.objects.filter(vendor=vendor, type='Vendor').order_by('-id')
                paginator = Paginator(vendor_reviews, 10)
                page = request.GET.get('page')
                paged_reviews = paginator.get_page(page)
                context = {
                    'vendor': vendor,
                    'reviews': paged_reviews,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def appointments(request, slug_txt):
    vendor = Vendor.objects.filter(slug=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated & isVendor(request.user):
            if vendor.login_id == request.user:
                appoi = Appointment.objects.filter(vendor=vendor).order_by('-id')
                filt = request.GET.get('filter')
                if filt == 'All' or filt is None:
                    filt = None
                else:
                    filt = str(filt)
                    if filt == 'approved':
                        appoi = appoi.filter(status=True)
                    if filt == 'not_approved':
                        appoi = appoi.filter(status=False)
                    elif filt == 'declined':
                        appoi = appoi.filter(declined=True)
                    elif filt == 'expired':
                        appoi = appoi.filter(expired=True)
                    elif filt == 'canceled':
                        appoi = appoi.filter(canceled=True)
                paginator = Paginator(appoi, 10)
                page = request.GET.get('page')
                paged_appoi = paginator.get_page(page)
                if filt is None:
                    filt = 'All'
                context = {
                    'selected_filter': filt,
                    'vendor': vendor,
                    'appointments': paged_appoi,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def bookings(request, slug_txt):
    vendor = Vendor.objects.filter(slug=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated & isVendor(request.user):
            if vendor.login_id == request.user:
                filt = request.GET.get('filter')
                bookgs = Booking.objects.filter(vendor=vendor).order_by('-id')
                if filt == 'All' or filt is None:
                    filt = None
                else:
                    filt = str(filt)
                    if filt == 'approved':
                        bookgs = bookgs.filter(status=True)
                    if filt == 'not_approved':
                        bookgs = bookgs.filter(status=False)
                    elif filt == 'declined':
                        bookgs = bookgs.filter(declined=True)
                    elif filt == 'expired':
                        bookgs = bookgs.filter(expired=True)
                    elif filt == 'canceled':
                        bookgs = bookgs.filter(canceled=True)
                paginator = Paginator(bookgs, 10)
                page = request.GET.get('page')
                paged_bookgs = paginator.get_page(page)
                if filt is None:
                    filt = 'All'
                context = {
                    'selected_filter': filt,
                    'vendor': vendor,
                    'bookings': paged_bookgs,
                    'not_count': getNotificationCount(vendor),
                    'chat_count': getChatCount(vendor)
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def approve_appointment(request, app_id):
    if request.user.is_authenticated & isVendor(request.user):
        vendor = Vendor.objects.get(login_id=request.user)
        appt = Appointment.objects.filter(vendor=vendor, id=app_id)
        if appt.exists():
            appt = appt.first()
            appt.status = True
            appt.declined = False
            appt.save()
            createNotification(
                title="The appointment you have with vendor {} at {}, from {}-{} was approved"
                    .format(appt.vendor, appt.date, appt.start_time, appt.end_time),
                typ=ty[1][0],
                user=appt.user,
                vendor=vendor
            )
            messages.success(request, "Appointment approved successfully")
            return redirect('vendor_appointments', vendor.slug)
        else:
            messages.error(request, "Approve failed, the appointment you choose does not belong to this vendor")
            return redirect('vendor_appointments', vendor.slug)
    return render(request, 'index.html')


def decline_appointment(request, app_id):
    if request.user.is_authenticated & isVendor(request.user):
        vendor = Vendor.objects.get(login_id=request.user)
        appt = Appointment.objects.filter(vendor=vendor, id=app_id)
        if appt.exists():
            appt = appt.first()
            appt.status = False
            appt.declined = True
            appt.save()
            createNotification(
                title="The appointment you have with vendor {} at {}, from {}-{} was declined"
                    .format(appt.vendor, appt.date, appt.start_time, appt.end_time),
                typ=ty[1][0],
                user=appt.user,
                vendor=vendor
            )
            messages.success(request, "Appointment declined")
            return redirect('vendor_appointments', vendor.slug)
        else:
            messages.error(request, "Decline failed, the appointment you choose does not belong to this vendor")
            return redirect('vendor_appointments', vendor.slug)
    return render(request, 'index.html')


def approve_booking(request, b_id):
    if request.user.is_authenticated & isVendor(request.user):
        vendor = Vendor.objects.get(login_id=request.user)
        booking = Booking.objects.filter(vendor=vendor, id=b_id)
        if booking.exists():
            booking = booking.first()
            booking.status = True
            booking.declined = False
            booking.save()
            createNotification(
                title="The booking you have with vendor {} at {}, from {}-{} was approved"
                    .format(booking.vendor, booking.date, booking.start_time, booking.end_time),
                typ=ty[1][0],
                user=booking.user,
                vendor=vendor
            )
            messages.success(request, "Booking approved successfully")
            return redirect('vendor_bookings', vendor.slug)
        else:
            messages.error(request, "Approve failed, the booking you choose does not belong to this vendor")
            return redirect('vendor_bookings', vendor.slug)
    return render(request, 'index.html')


def decline_booking(request, b_id):
    if request.user.is_authenticated & isVendor(request.user):
        vendor = Vendor.objects.get(login_id=request.user)
        booking = Booking.objects.filter(vendor=vendor, id=b_id)
        if booking.exists():
            booking = booking.first()
            booking.status = False
            booking.declined = True
            booking.save()
            createNotification(
                title="The booking you have with vendor {} at {}, from {}-{} was declined"
                    .format(booking.vendor, booking.date, booking.start_time, booking.end_time),
                typ=ty[1][0],
                user=booking.user,
                vendor=vendor
            )
            messages.success(request, "Booking declined")
            return redirect('vendor_bookings', vendor.slug)
        else:
            messages.error(request, "Approve failed, the booking you choose does not belong to this vendor")
            return redirect('vendor_bookings', vendor.slug)
    return render(request, 'index.html')


def chats(request, slug_txt):
    vendor = Vendor.objects.filter(slug=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated & isVendor(request.user):
            if vendor.login_id == request.user:
                query = "SELECT * FROM `Chat_chat` WHERE id IN (SELECT MAX(id)" \
                        " FROM Chat_chat WHERE vendor_id = {} GROUP BY `user_id`) " \
                        "ORDER BY `id` DESC".format(vendor.id)
                vendor_chats = Chat.objects.raw(query)
                context = {
                    'vendor': vendor,
                    'not_count': getNotificationCount(vendor),
                }
                user_chat_count = []
                for v_chat in vendor_chats:
                    user_chat_count.append(getChatCountWithUser(vendor, v_chat.user))
                if len(vendor_chats) > 0:
                    context['vendor_chats'] = vendor_chats
                    context['user_chat_counts'] = user_chat_count
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def markMsgUnread(chats):
    for chat in chats:
        if chat.sender == sender[1][0] and not chat.read_status:
            chat.read_status = True
            chat.save()


def vendor_user_chat(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated & isVendor(request.user):
            vendor = Vendor.objects.get(login_id=request.user)
            if vendor.login_id == request.user:
                query = "SELECT * FROM `Chat_chat` WHERE id IN (SELECT MAX(id)" \
                        " FROM Chat_chat WHERE vendor_id = {} GROUP BY `user_id`) " \
                        "ORDER BY `id` DESC".format(vendor.id)
                vendor_chats = Chat.objects.raw(query)
                vendor_user_chats = Chat.objects.filter(user=user, vendor=vendor)
                markMsgUnread(vendor_user_chats)
                context = {
                    'vendor': vendor,
                    'user': user,
                    'not_count': getNotificationCount(vendor),
                }
                user_chat_count = []
                for v_chat in vendor_chats:
                    user_chat_count.append(getChatCountWithUser(vendor, v_chat.user))
                if len(vendor_chats):
                    context['vendor_chats'] = vendor_chats
                if vendor_user_chats.exists():
                    context['vendor_user_chat'] = vendor_user_chats
                    context['user_chat_counts'] = user_chat_count
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def vendor_user_send_msg(request, slug_txt):
    if request.user.is_authenticated:
        if isVendor(request.user):
            if request.method == 'POST':
                users = Users.objects.filter(slug__iexact=slug_txt)
                if users.exists():
                    users = users.first()
                    vendor = Vendor.objects.get(login_id=request.user)
                    msg_content = str(request.POST['msg']).strip()
                    cht = Chat(message=msg_content, user=users, vendor=vendor, sender=sender[0][0])
                    cht.save()
                    return redirect('vendor_user_chat', users.slug)
                else:
                    return HttpResponse("Page Not Found")
            else:
                return HttpResponse("Page Not Found")
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def makeUnread(vendor):
    notir = Notification.objects.filter(vendor=vendor, type=ty[2][0], read_status=False).order_by('-id')
    for n in notir:
        if not n.read_status:
            n.read_status = True
            n.save()


def notification(request, slug_txt):
    vendor = Vendor.objects.filter(slug=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated & isVendor(request.user):
            if vendor.login_id == request.user:
                notif = Notification.objects.filter(vendor=vendor, type=ty[2][0]).order_by('-id')
                paginator = Paginator(notif, 10)
                page = request.GET.get('page')
                paged_not = paginator.get_page(page)
                context = {
                    'vendor': vendor,
                    'chat_count': getChatCount(vendor)
                }
                st = threading.Timer(5, makeUnread, (vendor,))
                st.start()
                if notif.exists():
                    context['notifications'] = paged_not
                return render(request, 'vendor/dashboard.html', context)
            else:
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
