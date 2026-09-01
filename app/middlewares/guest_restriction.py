from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from core.url_names import ACCOUNTS


class GuestRestrictionMiddleware:
    """
    Middleware that restricts unauthenticated users to only access 
    the root URL and the login page. Redirects all other paths to root.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_path = reverse(ACCOUNTS.AUTH.LOGIN)
        self.root_path = '/'
       
    def __call__(self, request):
        if not request.user.is_authenticated:
            current_path = request.path
            
            is_root = current_path == self.root_path
            is_login = current_path == self.login_path
            
            is_static_or_media = (
                current_path.startswith('/static/') or 
                current_path.startswith('/media/')
            )
            
            if not (is_root or is_login or is_static_or_media):
                return HttpResponseRedirect(self.root_path)

        return self.get_response(request)
