from django.forms import ModelForm
from Users.models import Users


class UsersForm(ModelForm):
    class Meta:
        model = Users
        exclude = ['login_id']
