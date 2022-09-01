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



class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    message = 'User Sign Up Successful'
    success_url = reverse_lazy('accounts:login')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:index')
        return super(SignUpView, self).dispatch(request,*args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    message = "Login Success"
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:index')
        return super(UserLoginView, self).dispatch(request,*args, **kwargs)


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('blog:index')
    message = "Password Changed Successfully"
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    message = "Password Reset Link has been sent to your mail. If not, try again with correct email address"
    success_url = reverse_lazy('accounts:login')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:blog_index')
        return super(UserPasswordResetView, self).dispatch(request,*args,**kwargs)


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')
    message = "Password Reset Success!"
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:blog_index')
        return super(UserPasswordResetConfirmView, self).dispatch(request,*args,**kwargs)