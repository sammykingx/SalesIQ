from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from core.url_names import ACCOUNTS


class OnboardingEnforcementMiddleware:
    """
    Middleware that ensures authenticated users have completed onboarding 
    before accessing the rest of the application. Allows access to onboarding 
    and email activation/verification routes (even with dynamic tokens).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.onboarding_path = reverse(ACCOUNTS.ONBOARDING)

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated:
            current_path = request.path
            
            is_onboarding_route = current_path == self.onboarding_path
            is_activation_route = current_path.startswith('/accounts/activation/')
            
            completed_onboarding = getattr(request.user, "onboarded", True)
            
            # If onboarding is incomplete, block everything except onboarding and activation pages
            if not completed_onboarding and not (is_onboarding_route or is_activation_route):
                return HttpResponseRedirect(self.onboarding_path)

        return self.get_response(request)
