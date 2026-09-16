from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView, View

from accounts.selectors import BusinessSelector
from core.template_names import APP_TEMPLATES
from customers.selectors import CustomerSelector
from customers.serializers import CreateCustomerSchema, CustomerMetricsSchema
from customers.repositories import CustomersRepo
from utils.pydantic_formatter import format_pydantic_errors

from pydantic import ValidationError
from typing import Any


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
            if biz_instance:
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
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "message": "The hamsters powering our servers just went on an unscheduled coffee break. We're waking them up.",
                "status": "error"
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
    