from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django import forms


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

    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ''
        }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("success_register")
    template_name = "auth-register.html"



def logout_view(request):
    logout(request)
    return redirect('/')


def success_register(request):
    return render(
        request,
        "success-register.html"
    )