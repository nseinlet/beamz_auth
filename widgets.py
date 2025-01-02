from urllib.parse import urlencode
from django import forms
from django.conf import settings


class TurnstileInput(forms.Widget):
    template_name = 'widgets/turnstile.html'

    def value_from_datadict(self, data, files, name):
        return data.get('cf-turnstile-response')

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-sitekey'] = settings.TURNSTILE_SITEKEY
        return attrs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['api_url'] = settings.TURNSTILE_JSAPIURL
        return context