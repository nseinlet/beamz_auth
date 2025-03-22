from urllib.parse import urlencode
from django import forms
from django.conf import settings


class CaptchaInput(forms.Widget):
    template_name = 'widgets/captcha.html'

    def value_from_datadict(self, data, files, name):
        if not hasattr(settings, 'CAPTCHA_SERVICE'):
            return False
        if settings.CAPTCHA_SERVICE == 'TURNSTILE':
            return data.get('cf-turnstile-response')
        return data.get('cf-captcha-response')

    def _captcha_class(self):
        if not hasattr(settings, 'CAPTCHA_SERVICE'):
            return ''
        if settings.CAPTCHA_SERVICE == 'CAPTCHAFOX':
            return 'captchafox'
        if settings.CAPTCHA_SERVICE == 'TURNSTILE':
            return 'cf-turnstile'
        return ''
    
    def _captcha_jsapiurl(self):
        if not hasattr(settings, 'CAPTCHA_SERVICE'):
            return ''
        if settings.CAPTCHA_SERVICE == 'CAPTCHAFOX':
            return "https://cdn.captchafox.com/api.js"
        if settings.CAPTCHA_SERVICE == 'TURNSTILE':
            return 'https://challenges.cloudflare.com/turnstile/v0/api.js' 
        return ''


    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-sitekey'] = settings.CAPTCHA_SERVICE_SITEKEY
        return attrs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['api_url'] = self._captcha_jsapiurl()
        context['captcha_class'] = self._captcha_class()
        return context
    