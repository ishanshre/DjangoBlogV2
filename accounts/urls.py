from django.urls import path
from .views import (
    SignUpView,
    UserLoginView,
    UserPasswordChangeView,
    UserPasswordResetView,
    UserPasswordResetConfirmView,
)
from django.contrib.auth.views import LogoutView


app_name = 'accounts'
urlpatterns = [
    path('register/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('password_change/',UserPasswordChangeView.as_view(), name="password_change"),
    path('password_reset/',UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/confirm/<uidb64>/<token>/',UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]