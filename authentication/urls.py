from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import RegistrationView, LogoutView, UsernameValidationView, RequestPasswordResetEmail, PasswordResetConfirmView, LoginView, EmailValidationView, ActivationView

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("validate_username", csrf_exempt( UsernameValidationView.as_view()), name="validate_username"),
    path("validate_email", csrf_exempt(EmailValidationView.as_view()), name="validate_email"),
    path("activate/<uidb64>/<token>", ActivationView.as_view(), name="activate"),
    path("request_reset_link", csrf_exempt(RequestPasswordResetEmail.as_view()), name="request_password"),
    path("reset_password_confirm/<uidb64>/<token>", PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
]

