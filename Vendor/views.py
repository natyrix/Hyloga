from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import AccountType, AcType
from .models import Vendor, Pricing, VendorImage
from .form import PricingForm, GalleryForm, LogoForm


def isVendor(user):
    vendor = Vendor.objects.filter(login_id=user)
    if vendor:
        return True
    else:
        return False


def dashboard(request, slug_txt):
    vendor = Vendor.objects.filter(slug__iexact=slug_txt)
    if vendor.exists():
        vendor = vendor.first()
        if request.user.is_authenticated:
            if vendor.login_id == request.user:
                context = {
                    'vendor': vendor
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                acType = AccountType.objects.get(user=request.user)
                if acType:
                    if acType.Actype == AcType[1][0]:  # Vendor
                        vendor = Vendor.objects.get(login_id=request.user)
                        return redirect('vendor_dashboard', vendor.slug)
                    elif acType.Actype == AcType[2][0]:  # Users
                        messages.success(request, "Just Logged in " + acType.Actype)
                        return render(request, 'accounts/login.html')

        else:
            return render(request, 'index.html')

    else:
        return HttpResponse("Page Not Found")

    return render(request, 'index.html')


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
                    'pricing_form': PricingForm
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                acType = AccountType.objects.get(user=request.user)
                if acType:
                    if acType.Actype == AcType[1][0]:  # Vendor
                        vendor = Vendor.objects.get(login_id=request.user)
                        return redirect('vendor_dashboard', vendor.slug)
                    elif acType.Actype == AcType[2][0]:  # Users
                        messages.success(request, "Just Logged in " + acType.Actype)
                        return render(request, 'accounts/login.html')

        else:
            return render(request, 'index.html')

    else:
        return HttpResponse("Page Not Found")

    return render(request, 'index.html')


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
            'pricing_form': form
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
                    'logo': vendor.logo
                }
                return render(request, 'vendor/dashboard.html', context)
            else:
                acType = AccountType.objects.get(user=request.user)
                if acType:
                    if acType.Actype == AcType[1][0]:  # Vendor
                        vendor = Vendor.objects.get(login_id=request.user)
                        return redirect('vendor_dashboard', vendor.slug)
                    elif acType.Actype == AcType[2][0]:  # Users
                        messages.success(request, "Just Logged in " + acType.Actype)
                        return render(request, 'accounts/login.html')

        else:
            return render(request, 'index.html')


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
                messages.warning(request, "Access Denied")
                return redirect('vendor_gallery', vendor.slug)
        else:
            messages.warning(request, "Image not found")
            return redirect('vendor_gallery', vendor.slug)

    else:
        return render(request, 'index.html')
