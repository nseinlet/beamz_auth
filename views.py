from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views import generic
from django.utils.translation import gettext as _

from .forms import UserRegisterForm, MissingTokenForm
from .models import UserValidation


class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("token_sent")
    template_name = "auth-register.html"

def missing_token(request):
    if request.method == "POST":
        form = MissingTokenForm(request.POST)
        if form.is_valid():
            uv = UserValidation.objects.filter(owner_uid__email=form.cleaned_data['email'])
            if uv.count()>0:
                uv.first().send_mail()
                return HttpResponseRedirect("/token-resent/")
    else:
        form = MissingTokenForm()

    return render(request, "missing-token.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')

def token_sent(request):
    return render(
        request,
        "token-sent.html"
    )

def token_resent(request):
    return render(
        request,
        "token-resent.html"
    )

def success_register(request):
    return render(
        request,
        "success-register.html"
    )

def activate_account(request, token):
    if not token:
        raise Http404(_("Account not activated, wrong token"))
    uv = UserValidation.objects.filter(owner_uid__is_active=False, auth_token=token)
    if uv.count()==0:
        raise Http404(_("Account not activated, wrong token"))
    user_reg = uv.first()
    uid = user_reg.owner_uid
    uid.is_active = True
    uid.save()
    user_reg.delete()
    return HttpResponseRedirect('/login/')
