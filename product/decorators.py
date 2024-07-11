# product/decorators.py
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

def hr_or_superuser_required(view_func):
    """
    Decorator for views that checks that the user is either HR or a superuser,
    displaying an alert message and redirecting to the same page if the user is not authorized.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='HR').exists()):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to access this page.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return _wrapped_view
