from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView, View

from accounts.domains.exceptions import AccountsDomainException
from accounts.selectors import BusinessSelector
from core.template_names import APP_TEMPLATES
from products.serializers import CreateProductsSchema
from products.domain.exceptions import ProductDomainException
from products.selectors import ProductsSelector
from products.service import ProductsService
from utils.pydantic_formatter import format_pydantic_errors

from pydantic import ValidationError
from typing import Any
import json


class CreateProductsView(LoginRequiredMixin, View):
    """
    Handles incoming HTTP POST requests to create a new product record 
    directly to the authenticated user's business.
    """
    biz_selector = BusinessSelector()
    

    def post(self, request: HttpRequest):
        try:
            data = CreateProductsSchema.model_validate_json(request.body, strict=True)
            ProductsService(request=request).add_product(product_data=data)
            return JsonResponse({
                "message": "",
                "status": "success"
            }, status=201)
            
        except ValidationError as err:
            return JsonResponse({
                "message": "Your data is looking a bit tragic. Fix your typos and try again.", 
                "error": format_pydantic_errors(err), 
                "status": "warning"
            }, status=422)
            
        except (AccountsDomainException, ProductDomainException) as err:
            return JsonResponse({
                "title": err.title,
                "message": err.message,
                "status": err.err_type,
            }, status=400)
            
        except Exception as err:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "message": "The hamsters powering our servers just went on an unscheduled coffee break. We're waking them up.",
                "status": "error"
            }, status=500)
          
            
class ProductsListView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.PRODUCTS.LIST
    product_selector = ProductsSelector()
    biz_selector = BusinessSelector()
    
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #      context = super().get_context_data(**kwargs)
    #      context.update(self.template_context())
    #      return context
     
    # def template_context(self) -> dict[str, Any]:
    #     products_data = []
    #     biz = BusinessSelector().get_user_business(user_email=self.request.user.email) # type:ignore
    #     if biz:
    #         products_data = self.product_selector.get_business_products(business_id=biz.id)
            
    #     return {
    #         "products_json": products_data,
    #     }
     
    