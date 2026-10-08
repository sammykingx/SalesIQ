from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from core.url_names import ACCOUNTS


class OnboardingEnforcementMiddleware:
    """
    Middleware that ensures authenticated users have completed onboarding 
    before accessing the rest of the application. Allows access to onboarding 
    and email activation/verification routes (even with dynamic tokens).
    
    Uses Django's built-in process_view hook.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.onboarding_path = reverse(ACCOUNTS.ONBOARDING)

    def __call__(self, request: HttpRequest):
        # if request.user.is_authenticated:
        #     current_path = request.path
            
        #     is_onboarding_route = current_path == self.onboarding_path
        #     is_activation_route = current_path.startswith('/accounts/activation/')
            
        #     completed_onboarding = getattr(request.user, "onboarded", True)
            
        #     # If onboarding is incomplete, block everything except onboarding and activation pages
        #     if not completed_onboarding and not (is_onboarding_route or is_activation_route):
        #         return HttpResponseRedirect(self.onboarding_path)

        return self.get_response(request)
    
    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs) -> HttpResponseRedirect | None:
        if request.user.is_authenticated:
            completed_onboarding = getattr(request.user, "onboarded", True)
            if not completed_onboarding:
                view_class = getattr(view_func, "view_class", None)
                should_skip_onboarding = getattr(view_class, "skip_onboarding_check", False) if view_class else False
                if not should_skip_onboarding:
                    return HttpResponseRedirect(self.onboarding_path)
            
        return None  # Continue processing the view normally
