import uuid
import hashlib
import logging

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from django_otp.plugins import otp_email, otp_totp

_logger = logging.getLogger(__name__)


def default_token():
    res = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()
    return res


class UserValidation(models.Model):
    owner_uid = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    auth_token = models.CharField(max_length=100, default=default_token)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner_uid.username
    
    def send_mail(self):
        html_message = render_to_string("mail_activation.html", {'token': self.auth_token, 'login': self.owner_uid.username})
        try:
            send_mail(_("Thanks for registering your BeamZ account"), strip_tags(html_message), None, [self.owner_uid.email], html_message=html_message)
        except Exception as e:
            _logger.error("Impossible to send email")
            _logger.error(e)
            return False
        return True


def get_otp_device(self):
    #Check if user have at least email as 2FA
    device = {
        'instance': None,
        'type': False,
    }

    if otp_totp.models.TOTPDevice.objects.filter(user=self).filter(confirmed=True).count() == 0:
        if otp_email.models.EmailDevice.objects.filter(user=self).count() == 0:
            device['instance'] = otp_email.models.EmailDevice.objects.create(user=self, confirmed=True)
            device['type'] = 'email'
        else:
            device['instance'] = otp_email.models.EmailDevice.objects.filter(user=self)[0]
            device['type'] = 'email'
    else:
        device['instance'] = otp_totp.models.TOTPDevice.objects.filter(user=self).filter(confirmed=True)[0]
        device['type'] = 'totp'
    if not device['instance']:
        raise Exception("Could not create OTP device")
        
    return device

def ensure_totp_device(self):
    if otp_totp.models.TOTPDevice.objects.filter(user=self).count() == 0:
        device = otp_totp.models.TOTPDevice.objects.create(user=self, confirmed=False)
    else:
        device = otp_totp.models.TOTPDevice.objects.filter(user=self)[0]
    if not device:
        raise Exception("Could not create TOTP device")
        
    return device

def reset_totp(self):
    for device in otp_totp.models.TOTPDevice.objects.filter(user=self).filter(confirmed=True):
        device.confirmed = False
        device.save()

User.add_to_class("get_otp_device", get_otp_device)
User.add_to_class("ensure_totp_device", ensure_totp_device)
User.add_to_class("reset_totp", reset_totp)
