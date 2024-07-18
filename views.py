from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserRegisterForm

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