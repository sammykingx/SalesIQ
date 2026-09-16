from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from urllib.parse import urlencode

from accounts.domains.exceptions import AccountsDomainException
from accounts.selectors import BusinessSelector
from core.template_names import APP_TEMPLATES
from core.url_names import PRODUCTS
from products.serializers import CreateProductsSchema, ModifyProductSchema, ProductListItemSchema
from products.domain.demo_data import PRODUCTS_DATA
from products.domain.exceptions import ProductDomainException
from products.selectors import ProductsSelector
from products.service import ProductsService
from utils.pydantic_formatter import format_pydantic_errors

from dataclasses import asdict
from pydantic import ValidationError
from typing import Any


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
                "message": "Product locked, loaded, and ready to sell. Our analytics engine are ready to start tracking data.",
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
            
            
class UpdateProductsView(LoginRequiredMixin, View):
    """
    Handles incoming HTTP PUT requests to update a new product record 
    directly to the authenticated user's business.
    """
    biz_selector = BusinessSelector()
    

    def put(self, request: HttpRequest):
        try:
            data = ModifyProductSchema.model_validate_json(request.body, strict=True)
            ProductsService(request=request).update_product(product_data=data)
            return JsonResponse({
                "message": "Product locked, loaded, and ready to sell. Our analytics engine are ready to start tracking data.",
                "status": "success",
                "redirect": True,
                "redirect_url": reverse(PRODUCTS.LIST),
            }, status=200)
            
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
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
         context = super().get_context_data(**kwargs)
         context.update(self.template_context())
         return context
     
    def template_context(self) -> dict[str, Any]:
        biz = BusinessSelector().get_user_business(user_email=self.request.user.email) # type:ignore
        products = self.product_selector.get_business_products(business_id=biz.id) # type:ignore
        products_data = [ProductListItemSchema.model_validate(product).model_dump() for product in products]
        
        return {
            "products_json": products_data,
        }
        
class ProductDetailView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.PRODUCTS.DETAIL
    product_selector = ProductsSelector()
    biz_selector = BusinessSelector()

    def dispatch(self, request, *args, **kwargs):
        p_ref = request.GET.get("p_ref")
        # merchant = request.GET.get("merchant")

        if not p_ref:
            return redirect(reverse(PRODUCTS.LIST))

        user_biz = self.biz_selector.get_user_business(user_email=request.user.email) #type: ignore
        
        if not user_biz:
            return redirect(reverse(PRODUCTS.LIST))

        product = self.product_selector.get_product_with_business(p_ref=p_ref)
        
        if not product or product.business_id != user_biz.id: #type:ignore
            return redirect(reverse(PRODUCTS.LIST))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self) -> dict:
        p_ref = self.request.GET.get("p_ref")
        product = self.product_selector.get_product(product_id=p_ref) #type:ignore
        return {
            "product": asdict(product), #type: ignore
            "p_ref": self.request.GET.get("p_ref"),
            "merchant": self.request.GET.get("merchant")
        }
        
     
QUERY_PARAMS = {
    "p_ref": "01a0883c1a6771dc89fc9358b6d26e8f",
    "merchant": "01a05b9dc4a079a9a13af8886e1a4c1c",
}
