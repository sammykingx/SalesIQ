"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from core.views import ComingSoonView
from core.template_names import APP_TEMPLATES
from core.url_names import PRODUCTS, SALES

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", ComingSoonView.as_view(), name="coming-soon"),
    path("accounts/", include("accounts.urls")),
    path("customers/", include("customers.urls")),
    path("products/", TemplateView.as_view(template_name=APP_TEMPLATES.PRODUCTS.LIST), name=PRODUCTS.LIST),
    path("sales/", TemplateView.as_view(template_name=APP_TEMPLATES.SALES.LIST), name=SALES.LIST),

    # invoices
]
