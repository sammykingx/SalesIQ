from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from core.url_names import ACCOUNTS


class OnboardingEnforcementMiddleware:
    """
    Middleware that ensures authenticated users have completed onboarding 
    before accessing the rest of the application.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.onboarding_path = reverse(ACCOUNTS.ONBOARDING)

    def __call__(self, request:HttpRequest):
        if request.user.is_authenticated:
            is_onboarding_route = request.path == self.onboarding_path
            completed_onboarding = getattr(request.user, "onboarded", True)
            
            if not completed_onboarding and not is_onboarding_route:
                return HttpResponseRedirect(self.onboarding_path)

        return self.get_response(request)
