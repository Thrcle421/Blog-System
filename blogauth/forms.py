from django import forms
from django.contrib.auth import get_user_model

from blogauth.models import ValidationModel
from blog.models import User


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'avatar']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_validation(self):
        validation = self.cleaned_data['validation']
        email = self.cleaned_data['email']
        validate = ValidationModel.objects.filter(
            email=email, validation=validation).first()
        if not validate:
            raise forms.ValidationError('This validation is incorrect.')
        validate.delete()
        return validation


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': 'Please enter your email',
                                             'invalid': 'Please enter a valid email'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)
