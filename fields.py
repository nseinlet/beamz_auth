import requests

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .widgets import CaptchaInput


class CaptchaField(forms.Field):
    widget = CaptchaInput

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['required'] = hasattr(settings, 'CAPTCHA_SERVICE') and settings.CAPTCHA_SERVICE!='' 
        return attrs

    def _captacha_verifyurl(self):
        if not hasattr(settings, 'CAPTCHA_SERVICE'):
            return ''
        if settings.CAPTCHA_SERVICE == 'CAPTCHAFOX':
            return "https://api.captchafox.com/siteverify"
        if settings.CAPTCHA_SERVICE == 'TURNSTILE':
            return 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        return ''


    def validate(self, value):
        if not hasattr(settings, 'CAPTCHA_SERVICE') or settings.CAPTCHA_SERVICE=='':
            return True
        super().validate(value)
        res = requests.post(
            url=self._captacha_verifyurl(),
            data={
                'secret': settings.CAPTCHA_SERVICE_SECRET if hasattr(settings, 'CAPTCHA_SERVICE_SECRET') else '',
                'response': value,
            },
        )
        res.raise_for_status()
        response_data = res.json()
        if not response_data.get('success'):
            raise ValidationError(_("Proove you're not a robot"))

