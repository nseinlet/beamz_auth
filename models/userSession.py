from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.db import models

# from importlib import import_module
# from django.conf import settings
# SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class UserSession(models.Model):
    owner_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    browser = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


def user_logged_in_handler(sender, request, user, **kwargs):
    # sess = Session.objects.get(session_key = request.session.session_key)
    # data = SessionStore().decode(sess.session_data)
    # print(data)

    UserSession.objects.get_or_create(
        owner_uid = user,
        session_id = Session.objects.get(session_key = request.session.session_key),
        browser = request.META.get('HTTP_USER_AGENT', ''),
        ip_address = request.META.get('REMOTE_ADDR', ''),
    )


user_logged_in.connect(user_logged_in_handler)
