from django.contrib import messages
from django.shortcuts import redirect

class AuthUserRestrictMixin:
    """This mixins restricts authenticated users to view pages like login, signup, forget password and so on"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("blog:index")
        return super().dispatch(request, *args, **kwargs)



class FormErrorMessageMixin:
    """This mixin displays the error messages"""
    error_message = None

    def form_invalid(self, form, *args, **kwargs):
        messages.add_message(self.request, messages.ERROR, self.error_message)
        return super().form_invalid(form, *args, **kwargs)