from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from accounts.selectors import UserSelector, BusinessSelector
from backoffice.mixins import BackofficeAccessMixin
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS

from typing import Any, Dict

import logging

logger = logging.getLogger(__name__)


class PlatformDashboardView(BackofficeAccessMixin, TemplateView):
    template_name = APP_TEMPLATES.BACKOFFICE.DASHBOARD
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
        
    def template_context(self) -> Dict[str, Any]:
        selector = BusinessSelector()
        recent_signups = selector.get_recent_signups(limit=7)
        platform_summary = selector.get_platform_summary()
            
        return {
            "recent_signups": recent_signups,
            **platform_summary,
        }
