from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from Vendor.models import Category, Vendor, st
from django.contrib import messages, auth
from Users.forms import UsersForm
from .models import AccountType, AcType


def validator(var):
    if len(var) == 0:
        return False
    else:
        return True


def registerCouple(request):
    if request.method == 'POST':
        return
    else:
        if request.user.is_authenticated:
            acType = AccountType.objects.get(user=request.user)
            if acType:
                if acType.Actype == AcType[1][0]:  # Vendor
                    vendor = Vendor.objects.get(login_id=request.user)
                    return redirect('vendor_dashboard', vendor.slug)
                elif acType.Actype == AcType[2][0]:  # Users
                    messages.success(request, "Just Logged in " + acType.Actype)
                    return render(request, 'accounts/login.html')
        context = {
            'form': UsersForm
        }
        return render(request, 'accounts/register_couple.html', context)


def registerVendor(request):
    if request.method == 'POST':
        name = str(request.POST['name']).strip()
        phone = str(request.POST['phone']).strip()
        address = str(request.POST['address']).strip()
        category = str(request.POST['category']).strip()
        email = str(request.POST['email']).strip()
        password = str(request.POST['password']).strip()
        password2 = str(request.POST['password2']).strip()
        if validator(name) & validator(phone) & validator(address) & validator(category) & validator(email) & validator(password) & validator(password2):
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already taken")
                    return redirect('register_vendor')
                else:
                    uname = email.split('@')
                    if User.objects.filter(username=uname[0]):
                        messages.error(request, "Email already taken")
                        return redirect('register_vendor')
                    else:
                        cat = Category.objects.get(category_name=category)
                        user = User.objects.create_user(email=email, username=uname[0], password=password)
                        user.save()
                        ac = AccountType(Actype=AcType[1][0], user=user)
                        ac.save()
                        vendor = Vendor(name=name, email=email,
                                        phonenumber=phone, address=address,
                                        status=st[1][0], category=cat, login_id=user)
                        vendor.save()
                        messages.success(request, "Registered successfully you can now login.")
                        return render(request, 'accounts/login.html')
            else:
                messages.error(request, "Passwords do not match")
                return redirect('register_vendor')
        else:
            messages.error(request, "Fields can not be empty")
            return redirect('register_vendor')
    else:
        if request.user.is_authenticated:
            acType = AccountType.objects.get(user=request.user)
            if acType:
                if acType.Actype == AcType[1][0]:  # Vendor
                    vendor = Vendor.objects.get(login_id=request.user)
                    return redirect('vendor_dashboard', vendor.slug)
                elif acType.Actype == AcType[2][0]:  # Users
                    messages.success(request, "Just Logged in " + acType.Actype)
                    return render(request, 'accounts/login.html')
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'accounts/register_vendor.html', context)


def login(request):
    if request.method == 'POST':
        email = str(request.POST['email']).strip()
        password = str(request.POST['password']).strip()
        if validator(email) & validator(password):
            username = email.split('@')
            user = auth.authenticate(username=username[0], password=password)
            if user is not None:
                acType = AccountType.objects.get(user=user)
                auth.login(request, user)
                if acType:
                    if acType.Actype == AcType[1][0]:#Vendor
                        vendor = Vendor.objects.get(login_id=user)
                        messages.success(request, "Successfully logged in")
                        return redirect('vendor_dashboard', vendor.slug)
                    elif acType.Actype == AcType[2][0]:#Users
                        messages.success(request, "Just Logged in " + acType.Actype)
                        return redirect('login')
                    elif acType.Actype == AcType[0][0]:#Admin
                        messages.success(request, "Just Logged in " + acType.Actype)
                        return redirect('login')
                else:
                    messages.error(request, "Something went wrong, if this error persists contact the admin")
                    return redirect('login')
            else:
                messages.error(request, "Wrong email or password")
                return redirect('login')
        else:
            messages.error(request, "Fields can not be empty")
            return redirect('login')
    else:
        if request.user.is_authenticated:
            acType = AccountType.objects.get(user=request.user)
            if acType:
                if acType.Actype == AcType[1][0]:  # Vendor
                    vendor = Vendor.objects.get(login_id=request.user)
                    return redirect('vendor_dashboard', vendor.slug)
                elif acType.Actype == AcType[2][0]:  # Users
                    messages.success(request, "Just Logged in " + acType.Actype)
                    return render(request, 'accounts/login.html')
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are logged out")
        return render(request, 'index.html')
