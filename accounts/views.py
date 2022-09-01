from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserLoginForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
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

    