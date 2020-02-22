from django.forms import ModelForm
from .models import Pricing, VendorImage, Vendor


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


class LogoForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['logo']

    def __init__(self, *args, **kwargs):
        super(LogoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

