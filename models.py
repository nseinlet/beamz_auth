import uuid
import hashlib

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _


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
        send_mail(_("Thanks for registering your BeamZ account"), strip_tags(html_message), None, [self.owner_uid.email], html_message=html_message)
