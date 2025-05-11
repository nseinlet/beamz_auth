import logging

from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import UserValidation, BlackList
from .fields import CaptchaField

_logger = logging.getLogger(__name__)


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': ''
        }))
    captcha = CaptchaField()


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(label=_('Old password'), widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    new_password1 = forms.CharField(label=_('New password'), widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    new_password2 = forms.CharField(label=_('Repeat new password'), widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    captcha = CaptchaField()
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if BlackList.objects.filter(email=data).count()>0:
            raise ValidationError(_("The account linked to this email is waiting activation."))
        if UserValidation.objects.filter(owner_uid__email=data).filter(owner_uid__is_active=False).count()==1:
            raise ValidationError(_("The account linked to this email is waiting Activation."))
        if User.objects.filter(email=data).count()>0:
            raise ValidationError(_("Invalid email address."))
        return data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()
        uv = UserValidation.objects.create(owner_uid=user)
        if not uv.send_mail():
            _logger.error("Impossible to send email, drop user validation. %s")
            uv.owner_uid.delete()
            uv.delete()
            raise Exception("Impossible to create user")
        return user


class MissingTokenForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if UserValidation.objects.filter(owner_uid__email=data).count()==0:
            raise ValidationError(_("Either your account is already validated, or you've not registered."))
        return data