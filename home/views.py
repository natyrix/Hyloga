from django.contrib import messages
from django.shortcuts import render, redirect

from Users.models import Users
from accounts.models import AccountType,AcType
from Vendor.models import Vendor


def index(request):
    if request.user.is_authenticated:
        acType = AccountType.objects.get(user=request.user)
        if acType:
            if acType.Actype == AcType[1][0]:  # Vendor
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
            elif acType.Actype == AcType[2][0]:  # Users
                users = Users.objects.get(login_id=request.user)
                return redirect('users_home', users.slug)
            elif acType.Actype == AcType[0][0]:  # Admin
                return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def about(request):
    if request.user.is_authenticated:
        acType = AccountType.objects.get(user=request.user)
        if acType:
            if acType.Actype == AcType[1][0]:  # Vendor
                vendor = Vendor.objects.get(login_id=request.user)
                return redirect('vendor_dashboard', vendor.slug)
            elif acType.Actype == AcType[2][0]:  # Users
                users = Users.objects.get(login_id=request.user)
                return redirect('users_home', users.slug)
            elif acType.Actype == AcType[0][0]:  # Admin
                return render(request, 'about.html')
    return render(request, 'about.html')
