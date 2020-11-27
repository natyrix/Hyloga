from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime
from Users.views import isUser, setExpired
from Vendor.models import Category, Vendor, st
from django.contrib import messages, auth
from rest_framework.authtoken.models import Token
from Vendor.views import isVendor, setExpiredVendor
from .forms import UsersForm
from .models import AccountType, AcType
from Users.models import Users


def validator(var):
    if len(var) == 0:
        return False
    else:
        return True


def registerCouple(request):
    if request.method == 'POST':
        couple_form = UsersForm(request.POST)
        if couple_form.is_valid():
            password = str(request.POST['password']).strip()
            password2 = str(request.POST['password2']).strip()
            if password == password2:
                email = couple_form.cleaned_data['email']
                if User.objects.filter(email=email).exists():
                    context = {
                        'form': couple_form
                    }
                    messages.error(request, "Email already taken")
                    return render(request, 'accounts/register_couple.html', context)
                else:
                    uname = email.split('@')
                    if User.objects.filter(username=uname[0]):
                        context = {
                            'form': couple_form
                        }
                        messages.error(request, "Email already taken")
                        return render(request, 'accounts/register_couple.html', context)
                    else:
                        first_name = couple_form.cleaned_data['first_name']
                        last_name = couple_form.cleaned_data['last_name']
                        role = couple_form.cleaned_data['role']
                        wedding_date = request.POST['wed_date']
                        fiance_first_name = couple_form.cleaned_data['fiance_first_name']
                        fiance_last_name = couple_form.cleaned_data['fiance_last_name']
                        fiance_email = couple_form.cleaned_data['fiance_email']
                        user = User.objects.create_user(email=email, username=uname[0], password=password)
                        user.save()
                        ac = AccountType(Actype=AcType[2][0], user=user)
                        ac.save()
                        users = Users(first_name=first_name, last_name=last_name,
                                      email=email, role=role,
                                      wedding_date=wedding_date,
                                      fiance_first_name=fiance_first_name,
                                      fiance_last_name=fiance_last_name,
                                      fiance_email=fiance_email, login_id=user
                                      )
                        users.save()
                        Token.objects.create(user=user)
                        messages.success(request, "Registered successfully you can now login.")
                        return render(request, 'accounts/login.html')
            else:
                context = {
                    'form': couple_form
                }
                messages.error(request, "Password do not match")
                return render(request, 'accounts/register_couple.html', context)
        else:
            context = {
                'form': UsersForm
            }
            messages.error(request, "Registering Failed")
            return render(request, 'accounts/register_couple.html', context)

    else:
        if request.user.is_authenticated:
            acType = AccountType.objects.get(user=request.user)
            if acType:
                if acType.Actype == AcType[1][0]:  # Vendor
                    vendor = Vendor.objects.get(login_id=request.user)
                    return redirect('vendor_dashboard', vendor.slug)
                elif acType.Actype == AcType[2][0]:  # Users
                    users = Users.objects.get(login_id=request.user)
                    return redirect('users_home', users.slug)
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
                    users = Users.objects.get(login_id=request.user)
                    return redirect('users_home', users.slug)
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
                        setExpiredVendor(vendor)
                        messages.success(request, "Successfully logged in")
                        return redirect('vendor_dashboard', vendor.slug)
                    elif acType.Actype == AcType[2][0]:#Users
                        users = Users.objects.get(login_id=user)
                        setExpired(users)
                        messages.success(request, "Successfully logged in")
                        return redirect('users_home', users.slug)
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
                    users = Users.objects.get(login_id=request.user)
                    return redirect('users_home', users.slug)
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        # us = Users.objects.all()
        # for u in us:
        #     Token.objects.create(user=u.login_id)
        auth.logout(request)
        messages.success(request, "You are logged out")
        return render(request, 'index.html')
