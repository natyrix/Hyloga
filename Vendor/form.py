from django.forms import ModelForm
from .models import Pricing, VendorImage, Vendor
from django.contrib.auth.models import User


class PricingForm(ModelForm):
    class Meta:
        model = Pricing
        exclude = ['vendor']

    def __init__(self, *args, **kwargs):
        super(PricingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GalleryForm(ModelForm):
    class Meta:
        model = VendorImage
        exclude = ['vendor']

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'


class LogoForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['logo']

    def __init__(self, *args, **kwargs):
        super(LogoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'


class AccountForm(ModelForm):
    class Meta:
        model = Vendor
        exclude = ['logo', 'slug', 'login_id', 'status']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'

