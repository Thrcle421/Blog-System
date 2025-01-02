from django import forms
from django.contrib.auth import get_user_model

from blogauth.models import ValidationModel

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': 'Please enter your username',
        'min_length': 'username must be at least 2 characters long',
        'max_length': 'username must be at most 20 characters long',
    })
    email = forms.EmailField(error_messages={'required': 'Please enter your email',
                                             'invalid': 'Please enter a valid email'})
    validation = forms.CharField(max_length=4,min_length=4)
    password = forms.CharField(max_length=20,min_length=6)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_validation(self):
        validation = self.cleaned_data['validation']
        email = self.cleaned_data['email']
        validate = ValidationModel.objects.filter(email=email, validation=validation).first()
        if not validate:
            raise forms.ValidationError('This validation is incorrect.')
        validate.delete()
        return validation

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': 'Please enter your email',
                                             'invalid': 'Please enter a valid email'})
    password = forms.CharField(max_length=20,min_length=6)
    remember = forms.IntegerField(required=False)



