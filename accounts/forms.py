from django.forms import ModelForm
from Users.models import Users


class UsersForm(ModelForm):
    class Meta:
        model = Users
        exclude = ['login_id', 'wedding_date', 'slug']

    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'

