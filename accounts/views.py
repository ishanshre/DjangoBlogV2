from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserLoginForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView
)
from django.urls import reverse_lazy

from accounts.mixins import AuthUserRestrictMixin, FormErrorMessageMixin



class SignUpView(AuthUserRestrictMixin, SuccessMessageMixin, FormErrorMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    message = 'User Sign Up Successful'
    success_url = reverse_lazy('accounts:login')
    error_message = "User Registration Error"

    def get_success_url(self) -> str:
        return reverse_lazy("accounts:login")

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    

class UserLoginView(AuthUserRestrictMixin, SuccessMessageMixin, FormErrorMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    message = "Login Success"
    error_message= "User login errror"


    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, FormErrorMessageMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('blog:index')
    message = "Password Changed Successfully"
    error_message = "User Password Change Failed"

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message


class UserPasswordResetView(AuthUserRestrictMixin, SuccessMessageMixin, FormErrorMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    message = "Password Reset Link has been sent to your mail. If not, try again with correct email address"
    error_message = "Failure to send the reset link"
    success_url = reverse_lazy('accounts:login')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message


class UserPasswordResetConfirmView(AuthUserRestrictMixin, SuccessMessageMixin, FormErrorMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')
    message = "Password Reset Success!"
    error_message = "Password reset failed"
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message