from django.contrib import admin

from .models.userValidation import UserValidation
from .models.userSession import UserSession


@admin.register(UserValidation)
class UserValidationAdmin(admin.ModelAdmin):
    list_display = [ 'owner_uid', 'created_at' ]

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = [ 'owner_uid', 'session_id', 'ip_address', 'browser', 'created_at' ]