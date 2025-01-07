import requests

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .widgets import TurnstileInput

class TurnstileField(forms.Field):
    widget = TurnstileInput

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['required']=not settings.DEBUG
        return attrs
    
    def validate(self, value):
        if settings.DEBUG:
            return True
        super().validate(value)
        res = requests.post(
            url=settings.TURNSTILE_VERIFYURL,
            data={
                'secret': settings.TURNSTILE_SECRET,
                'response': value,
            },
        )
        res.raise_for_status()
        response_data = res.json()
        if not response_data.get('success'):
            raise ValidationError(_("Proove you're not a robot"))
