import logging

from django.db import models

_logger = logging.getLogger(__name__)


class BlackList(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.email
    