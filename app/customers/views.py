from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, View

from accounts.selectors import BusinessSelector
from core.template_names import APP_TEMPLATES
from core.url_names import CUSTOMERS
from customers.selectors import CustomerSelector
from customers.serializers import CreateCustomerSchema, CustomerMetricsSchema
from customers.repositories import CustomersRepo
from invoices.selectors import InvoiceMerchantSelector
from utils.pydantic_formatter import format_pydantic_errors

from pydantic import ValidationError
from typing import Any

import logging


logger = logging.getLogger(__name__)


class CreateCustomersView(LoginRequiredMixin, View):
    """
    Handles incoming HTTP POST requests to create a new customer record 
    and link them directly to the authenticated user's business.
    """
    biz_selector = BusinessSelector()
    buisness_clients_selector = CustomerSelector()

    def post(self, request: HttpRequest):
        try:
            data = CreateCustomerSchema.model_validate_json(request.body, strict=True)
            biz_instance = self.biz_selector.get_user_business(user_email=request.user.email, as_instance=True) # type: ignore
            if not biz_instance:
                return JsonResponse({
                    "message": "No registered business found. Please create a business profile before adding customers.",
                    "status": "error"
                }, status=200)
                
            CustomersRepo().create_and_link_customer(
                business=biz_instance, customer_data=data, display_name=data.display_name # type: ignore
            ) 
            
            return JsonResponse({
                "message": "Customer successfully trapped in your business ecosystem. Another soul joins the fold!",
                "status": "success"
            }, status=201)

        except ValidationError as err:
            return JsonResponse({
                "message": "Your data is looking a bit tragic. Fix your typos and try again.", 
                "error": format_pydantic_errors(err), 
                "status": "error"
            }, status=422)
            
        except Exception as err:
            logger.exception(
                "Failed to create customer for business owner '%s': %s",
                getattr(request.user, "email", "unknown"),
                err,
            )
            return JsonResponse({
                "title": "System Notice",
                "message": "We encountered an unexpected issue on our end. Our team has been notified, but please try again shortly.",
                "status": "error",
            }, status=500)
          
            
class BusinessCustomersListView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.CUSTOMERS.LIST
    biz_selector = BusinessSelector()
    buisness_clients_selector = CustomerSelector()
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
         context = super().get_context_data(**kwargs)
         context.update(self.template_context())
         return context
     
    def template_context(self) -> dict[str, Any]:
        biz = self.biz_selector.get_user_business(user_email=self.request.user.email) # type: ignore
        customers_data = self.buisness_clients_selector.get_all_business_customers_frontend_json(biz_id=biz.id) #type: ignore
        metrics = self.buisness_clients_selector.get_business_customer_metrics(biz_id=biz.id) #type: ignore
        metrics_data = CustomerMetricsSchema.model_validate(metrics).model_dump()
        
        return {
            "customers_json": customers_data,
            "metrics": metrics_data,
        }
        
        
class CustomerDetailView(LoginRequiredMixin, View):
    template_name = APP_TEMPLATES.CUSTOMERS.DETAIL
    biz_selector = BusinessSelector()
    buisness_clients_selector = CustomerSelector()
    business = None
    slug = None
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        slug = kwargs.get("slug")
        business = self.biz_selector.get_user_business(
            user_email=self.request.user.email,     # type: ignore
            as_instance=True
        )
        
        if not self.buisness_clients_selector.ensure_valid_business_customer_slug(
            biz_instance=business, slug=slug        # type: ignore
        ):
            return redirect(reverse(CUSTOMERS.LIST))
        
        self.business = business
        self.slug = slug
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        customer_data = self.buisness_clients_selector.get_single_for_business(
            biz=self.business, slug=self.slug
        )
        
        customers_profile_json = customer_data.to_dict() if customer_data else {}
        transaction_record = InvoiceMerchantSelector().get_customer_recent_sale_summary(
            business_id=customer_data.business_id,  # type:ignore
            client_id=customer_data.customer.id     # type:ignore
        )

        customers_profile_json.update(transaction_record)
        
        ctx = {"customer_json": customers_profile_json, "profile_slug": self.slug }
        
        return render(
            request=request,
            template_name=self.template_name,
            context=ctx,
        )
        
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            data = CreateCustomerSchema.model_validate_json(request.body, strict=True)
            CustomersRepo().update_business_customer_info(
                business_id=self.business.id, #type:ignore
                customer_data=data,
                profile_slug=self.slug
            )
            
            return JsonResponse({
                "title": "All Set! ✨",
                "message": "Client profile updated successfully. Your local changes are now live.",
                "status": "success",
                
            }, status=200)

        except ValidationError as err:
            return JsonResponse({
                "title": "Oops, Try Again",
                "message": "Invalid details provided. Please check your inputs and try again.", 
                "error": format_pydantic_errors(err), 
                "status": "error"
            }, status=422)
            
        except Exception as err:
            logger.exception(
                "Failed to update customer profile for business '%s': %s",
                getattr(self.business, "code", "unknown"),
                err,
            )
            return JsonResponse({
                "title": "System Notice",
                "message": "We encountered an unexpected issue on our end. Our team has been notified, but please try again shortly.",
                "status": "error",
            }, status=500)
