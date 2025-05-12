import logging
import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.forms import OTPTokenForm
from django_otp.qr import write_qrcode_image

from .forms import UserRegisterForm, MissingTokenForm
from .models import UserValidation

_logger = logging.getLogger(__name__)


class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("token_sent")
    template_name = "auth-register.html"

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except:
            form = UserRegisterForm(request.POST)
            return render(request, self.template_name, {"form": form, "extra_error": _('Error while creating user. Check email adress or username.')})


def missing_token(request):
    extra_error = ""
    if request.method == "POST":
        form = MissingTokenForm(request.POST)
        if form.is_valid():
            uv = UserValidation.objects.filter(owner_uid__email=form.cleaned_data['email'], owner_uid__is_active=False)
            if uv.count()>0:
                if uv.first().send_mail():
                    return HttpResponseRedirect("/token-resent/")
                else:
                    extra_error = _("There was an issue sending email. Is your address correct?")
    else:
        form = MissingTokenForm()

    return render(request, "missing-token.html", {"form": form, "extra_error": extra_error})

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

@login_required
def otp(request):
    def _redirect(request):
        redirect_url = request.GET.get('next', False)
        if not redirect_url:
            redirect_url = settings.LOGIN_REDIRECT_URL
        return redirect(redirect_url)
    
    if request.user.is_verified():
        return _redirect(request)

    #Ensure user have at least the email device if no other available
    device = request.user.get_otp_device()
    form = OTPTokenForm(request.user)
    error_msg = ""
    if request.method == "POST":
        token = False
        if 'otp_token' in request.POST:
            token = request.POST.get('otp_token')
        else:
            post_data = json.loads(request.body.decode("utf-8"))
            token = post_data['otp_token']
        try:
            with transaction.atomic():
                form.user.otp_device = form._verify_token(request.user, token, device['instance'])
                request.session[DEVICE_ID_SESSION_KEY] = form.user.otp_device.persistent_id
                return _redirect(request)
        except ValidationError as e:
            error_msg = e.message
    else:
        form = OTPTokenForm(request.user)
        if device['type'] == 'email':
            device['instance'].generate_challenge()

    return render(request, "auth-otp.html", {"form": form, "device": device, "error_msg": error_msg})

@login_required
def otp_new_challenge(request):
    if request.method == "POST":
        device = request.user.get_otp_device()
        if device['type'] == 'email':
            device['instance'].generate_challenge()
            return JsonResponse({"generated": True})
    return JsonResponse({"generated": False})

@login_required
def otp_totp_qr_code(request):
    device = request.user.ensure_totp_device()
    response = HttpResponse(content_type='image/svg+xml')
    write_qrcode_image(device.config_url, response)
    return response

@login_required
def otp_totp_check(request):
    device = request.user.ensure_totp_device()
    if request.method == "POST":
        token = False
        if 'otp_token' in request.POST:
            token = request.POST.get('otp_token')
        else:
            post_data = json.loads(request.body.decode("utf-8"))
            token = post_data['otp_token']
        try:
            with transaction.atomic():
                device.confirmed = device.verify_token(token)
                device.save()
        except ValidationError as e:
            error_msg = e.message

    return JsonResponse({"checked": device.confirmed})


@login_required
def otp_totp_settings(request):
    device = request.user.get_otp_device()

    return JsonResponse({"type": device['type']})