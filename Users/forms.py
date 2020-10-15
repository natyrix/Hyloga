from django.db.models.expressions import RawSQL
from django.forms import ModelForm
from django import forms
import datetime

from AppointmentandBooking.models import Appointment
from Users.models import Users, CheckList, ImageGallery, VideoGallery, UsersVideo, UsersImage, Budget
from Vendor.models import Category


class UsersForm(ModelForm):
    class Meta:
        model = Users
        exclude = ['login_id']


class ImageForm(ModelForm):
    class Meta:
        model = UsersImage
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'


class VideoForm(ModelForm):
    class Meta:
        model = UsersVideo
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'


class CheckListForm(ModelForm):
    class Meta:
        model = CheckList
        exclude = ['user', 'date_and_time', 'status']

    def __init__(self, *args, **kwargs):
        super(CheckListForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AccountForm(ModelForm):
    class Meta:
        model = Users
        exclude = ['slug', 'login_id', 'wedding_date']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'


class CategoryForm(ModelForm):
    class Meta:
        model = Budget
        exclude = ['vendors', 'prices', 'user']

    qset = Category.objects.filter(id__in=RawSQL(
        "SELECT category_id FROM Vendor_vendor", []
    ))
    choices = [
        ('All', 'Top 10 (All)'), ('best_1', 'Top 1'), ('best_of_3', 'Top 3'), ('best_of_5', 'Top 5')
    ]
    vendor_categories = forms.ModelMultipleChoiceField(queryset=qset,
                                                       widget=forms.SelectMultiple())
    sort = forms.ChoiceField(choices=choices, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'