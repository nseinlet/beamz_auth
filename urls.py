from django.contrib.auth import views
from django.urls import path

from .views import UserLoginForm, logout_view, ResetPasswordForm, SignUpView

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
    path('change-password/', views.PasswordChangeView.as_view()),
    path('reset-password/', views.PasswordResetView.as_view(template_name="password_reset_form.html", form_class=ResetPasswordForm), name="password_reset"),
    path('reset-password-sent/', views.PasswordResetView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name="reset_password_form.html"), name='password_reset_confirm'),
    path('reset-password-complete/', views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
    path("register/", SignUpView.as_view(), name="register"),
]