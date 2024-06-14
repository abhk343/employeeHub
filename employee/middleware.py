# employee/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that ensures the user is logged in for every request.
    Exclude login, admin, and static URLs.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith(reverse('login')):
            if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
                return redirect('login')
        response = self.get_response(request)
        return response
