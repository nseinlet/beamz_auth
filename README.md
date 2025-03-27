# beamz_auth
Django auth forms using bootstrap

Handle validation of user registration, as well as sessions listing.

# Installation
```bash

pip install -r requirements.txt

```

# Captcha

Use a captcha service to prevent spam registrations.
Tested services are Captchafox and Turnstile

To use them, you need to set the given settings:
```python
# settings.py
CAPTCHA_SERVICE = 'CAPTACHAFOX'  # or 'TURNSTILE'
CAPTCHA_SERVICE_SITEKEY = 'your_captcha_service_key'
CAPTCHA_SERVICE_SECRET = 'your_captcha_service_secret'
```
if `CAPTCHA_SERVICE` is not set, the captcha will not be used.
