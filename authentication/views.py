from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .email_service import send_activation_email


# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]

        if not validate_email(email, check_mx=False):
            return JsonResponse({"email_error":"Email is invalid"}, status=400)
    
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error":"Sorry, this email is already taken"}, status=409)
        
        return JsonResponse({"validate_email": True})
    

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error":"Username should only contain alphanumeric characters"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error":"Sorry, this username is already taken"}, status=409)
        
        return JsonResponse({"username_valid": True})
    
class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")
    
    def post(self, request):
        # Get user data
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {
            "fieldValues": request.POST
        }

        # Validate user data
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, "Password too short")
                    return render(request, "authentication/register.html" , context)
                # Create a user account
                try:
                    user = User.objects.create_user(
                        username=username, 
                        email=email,
                        password=password,
                        is_active = False,
                        )
                    
                    
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    activation_path = reverse("activate", kwargs={"uidb64":uid, "token": token})
                    activation_url = request.build_absolute_uri(activation_path)

                    #Send activation email
                    if send_activation_email(user.email, activation_url, user.username):
                        messages.success(request, "Check your email to activate your account")
                        return render(request, "authentication/register.html")
                        
                    else:
                        messages.error(request, "Failed to send activation email")
                        user.delete()
                        return render(request, "authentication/register.html", context)
                except Exception as e:
                    messages.error(request, f"Account creation failed: {str(e)}")
                    return render(request, "authentication/register.html", context)
              
    

               


class ActivationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully")
                return redirect("login")
                # return render(request, "authentication/login.html")
            messages.error(request, "Activation link is invalid")
            return render(request, "authentication/register.html")
        
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Activation link is invalid")
            return render(request, "authentication/register.html")
        
class LoginView(View):
    
    def get(self, request):
        return render(request, "authentication/login.html")
    
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome " + user.username + " you are now logged in")
                    return redirect("index")
                messages.error(request, "Your account is not active, check your email for the verification link")
                return render(request, "authentication/login.html")
            messages.error(request, "Invalid Credentials, try again")
            return render(request, "authentication/login.html")
        messages.error(request, "Please fill all fields")
        return render(request, "authentication/login.html")
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect("login")
            