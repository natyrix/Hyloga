from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Vendor.models import Vendor, st, VendorImage
from accounts.models import AccountType, AcType
from .models import Users
from RateandReview.models import Rate


def isUser(user):
    us = Users.objects.filter(login_id=user)
    if us:
        return True
    else:
        return False


def home(request, slug_txt):
    user = Users.objects.filter(slug__iexact=slug_txt)
    if user.exists():
        user = user.first()
        if request.user.is_authenticated:
            if user.login_id == request.user:
                context = {
                    'users': user
                }
                return render(request, 'users/home.html', context)
            else:
                acType = AccountType.objects.get(user=request.user)
                if acType:
                    if acType.Actype == AcType[1][0]:  # Vendor
                        vendor = Vendor.objects.get(login_id=request.user)
                        return redirect('vendor_dashboard', vendor.slug)
                    elif acType.Actype == AcType[2][0]:  # Users
                        users = Users.objects.get(login_id=user)
                        return redirect('users_home', users.slug)
                    else:
                        return render(request, 'index.html')
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
                vendors = Vendor.objects.filter(status=st[0][0]).order_by('-id')
                paginator = Paginator(vendors, 4)
                page = request.GET.get('page')
                paged_vendors = paginator.get_page(page)
                context = {
                    'users': user,
                    'vendors': paged_vendors,
                }
                return render(request, 'users/home.html', context)
            else:
                acType = AccountType.objects.get(user=request.user)
                if acType:
                    if acType.Actype == AcType[1][0]:  # Vendor
                        vendor = Vendor.objects.get(login_id=request.user)
                        return redirect('vendor_dashboard', vendor.slug)
                    elif acType.Actype == AcType[2][0]:  # Users
                        users = Users.objects.get(login_id=user)
                        return redirect('users_home', users.slug)
                    else:
                        return render(request, 'index.html')
        else:
            return render(request, 'index.html')
    else:
        return HttpResponse("Page Not Found")


def users_vendor(request, id):
    if request.user.is_authenticated & isUser(request.user):
            vendor = Vendor.objects.filter(pk=id)
            if vendor.exists():
                vendor = vendor.first()
                users = Users.objects.get(login_id=request.user)
                vendor_images = VendorImage.objects.filter(vendor=vendor)
                vendor_ratings = Rate.objects.filter(vendor=vendor)
                context = {
                    'users': users,
                    'vendor': vendor,
                }
                if vendor_images.exists():
                    context['vendor_images'] = vendor_images
                if vendor_ratings.exists():
                    sum = 0
                    for rating in vendor_ratings:
                        sum += int(rating.rate_value)
                    avg = sum/vendor_ratings.count()
                    p_cal = 100/vendor_ratings.count()
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
