from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from core.url_names import ACCOUNTS
from typing import Any

import logging


logger = logging.getLogger(__name__)


class BackofficeAccessMixin(LoginRequiredMixin):
    """
    Restricts access to class-based views exclusively to privileged backoffice users.
    
    This mixin extends `LoginRequiredMixin` to ensure the user is authenticated 
    before performing email-based whitelist validation. 
    
    Attributes:
        skip_onboarding_check (bool): Flag used by the onboarding enforcement 
            middleware to determine that users accessing this view are exempt 
            from mandatory onboarding completion requirements.
    
    Behavior:
        - If the authenticated user's email is present in `settings.PREVILEDGE_USERS`, 
          access is granted, and the request proceeds normally.
        - If the user's email is not in the privileged list, a warning is logged, 
          and the user is redirected to the accounts dashboard (`ACCOUNTS.DASHBOARD`).
    """
    skip_onboarding_check = True
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = request.user
        user_email = getattr(user, "email", "Unkown")
        if user_email not in settings.PREVILEDGE_USERS:
            logger.warning(f"User {user_email} is not a privileged user")
            return redirect(reverse(ACCOUNTS.DASHBOARD))
                
        return super().dispatch(request, *args, **kwargs)
