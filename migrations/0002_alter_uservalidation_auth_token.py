# Generated by Django 5.1.2 on 2024-11-12 17:13

import beamz_auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beamz_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservalidation',
            name='auth_token',
            field=models.CharField(default=beamz_auth.models.userValidation.default_token, max_length=100),
        ),
    ]
