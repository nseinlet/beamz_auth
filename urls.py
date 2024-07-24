from django.contrib.auth import views
from django.urls import path

from .forms import UserLoginForm, ResetPasswordForm, ChangePasswordForm
from .views import logout_view, SignUpView, success_register, token_sent, missing_token, activate_account


urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(
            template_name="auth-login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
    ),
    path('logout/', logout_view, name='logout'),
    path('change-password/', views.PasswordChangeView.as_view(template_name="change_password_form.html", form_class=ChangePasswordForm)),
    path('reset-password/', views.PasswordResetView.as_view(template_name="password_reset_form.html", form_class=ResetPasswordForm), name="password_reset"),
    path('reset-password-sent/', views.PasswordResetView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name="reset_password_form.html"), name='password_reset_confirm'),
    path('reset-password-complete/', views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
    path("register/", SignUpView.as_view(), name="register"),
    path("missing-token/", missing_token, name="missing_token"),
    path("token-sent/", token_sent, name="token_sent"),
    path("token-resent/", token_sent, name="token_resent"),
    path("successregister/", success_register, name="success_register"),
    path('activate/<token>/',  activate_account, name='activate_account'),
]