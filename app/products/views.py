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
from products.serializers import CreateProductsSchema, ModifyProductSchema
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
            # ProductsService(request=request).add_product(product_data=data)
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
        products_data = []
        biz = BusinessSelector().get_user_business(user_email=self.request.user.email) # type:ignore
        if biz:
            products_data = self.product_selector.get_business_products(business_id=biz.id)
        
        
        main_endpoint = reverse_lazy(PRODUCTS.DETAIL)
        qs=f"{main_endpoint}?{urlencode(QUERY_PARAMS)}"
        
        return {
            "products_json": PRODUCTS_DATA,
        }
        
class ProductDetailView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.PRODUCTS.DETAIL
    product_selector = ProductsSelector()
    biz_selector = BusinessSelector()

    def dispatch(self, request, *args, **kwargs):
        p_ref = request.GET.get("p_ref")
        merchant = request.GET.get("merchant")

        if not p_ref or not merchant:
            return redirect(reverse(PRODUCTS.LIST))

        user_biz = self.biz_selector.get_user_business(user_email=request.user.email) #type: ignore
        
        if not user_biz:
            return redirect(reverse(PRODUCTS.LIST))

        product = self.product_selector.get_product_with_business(p_ref=p_ref)
        
        if not product or product.business_id != user_biz.id: #type:ignore
            return redirect(reverse(PRODUCTS.LIST))

        # if str(product.business.id) != merchant:
        #     return redirect(reverse(PRODUCTS.LIST))

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



PRODUCTS_DATA = [
    { "id": 1, "name": "Pro Wireless Headphones", "price": 199.99, "product_type": "physical", "status": "Active", "dateAdded": "2026-08-12", "salesCount": 142, "url": "/products/detail/?p_ref=01a0883c1a6771dc89fc9358b6d26e8f&merchant=01a05b9dc4a079a9a13af8886e1a4c1c" },
    { "id": 2, "name": "Digital Marketing Playbook (PDF)", "price": 49.00, "product_type": "digital", "status": "Active", "dateAdded": "2026-08-10", "salesCount": 389, "url": "/products/2" },
    { "id": 3, "name": "Ergonomic Mechanical Keyboard", "price": 129.50, "product_type": "service", "status": "Active", "dateAdded": "2026-08-05", "salesCount": 88, "url": "/products/3" },
    { "id": 4, "name": "SaaS UI Component Kit License", "price": 89.00, "product_type": "digital", "status": "Active", "dateAdded": "2026-07-28", "salesCount": 612, "url": "/products/4" },
    { "id": 5, "name": "Minimalist Leather Desk Pad", "price": 35.00, "product_type": "digital", "status": "Active", "dateAdded": "2026-07-22", "salesCount": 54, "url": "/products/5" },
    { "id": 6, "name": "1-on-1 Business Coaching (1hr)", "price": 150.00, "product_type": "service", "status": "Active", "dateAdded": "2026-07-15", "salesCount": 29, "url": "/products/6" },
    { "id": 7, "name": "Smart Fitness Tracker Watch", "price": 89.99, "product_type": "physical", "status": "Inactive", "dateAdded": "2026-07-01", "salesCount": 210, "url": "/products/7" },
    { "id": 8, "name": "SEO Optimization Video Course", "price": 119.00, "product_type": "digital", "status": "Active", "dateAdded": "2026-06-25", "salesCount": 175, "url": "/products/8" },
    { "id": 9, "name": "Aluminum Laptop Stand", "price": 42.50, "product_type": "service", "status": "Active", "dateAdded": "2026-06-18", "salesCount": 95, "url": "/products/9" },
    { "id": 10, "name": "Lightroom Preset Bundle", "price": 29.99, "product_type": "physical", "status": "Active", "dateAdded": "2026-06-12", "salesCount": 430, "url": "/products/10" },
    { "id": 11, "name": "Noise-Canceling Earbuds", "price": 110.00, "product_type": "physical", "status": "Active", "dateAdded": "2026-06-02", "salesCount": 112, "url": "/products/11" },
    { "id": 12, "name": "E-commerce Notion Template", "price": 19.00, "product_type": "digital", "status": "Active", "dateAdded": "2026-05-29", "salesCount": 820, "url": "/products/12" },
    { "id": 13, "name": "USB-C Docking Station 11-in-1", "price": 79.99, "product_type": "physical", "status": "Active", "dateAdded": "2026-05-15", "salesCount": 67, "url": "/products/13" },
    { "id": 14, "name": "Custom Logo Design Package", "price": 299.00, "product_type": "service", "status": "Active", "dateAdded": "2026-05-01", "salesCount": 43, "url": "/products/14" },
    { "id": 15, "name": "HD Webcam with Dual Mic", "price": 59.95, "product_type": "physical", "status": "Active", "dateAdded": "2026-04-20", "salesCount": 158, "url": "/products/15" },
    { "id": 16, "name": "Podcast Sound Effect Library", "price": 39.00, "product_type": "physical", "status": "Inactive", "dateAdded": "2026-04-10", "salesCount": 94, "url": "/products/16" },
    { "id": 17, "name": "Vertical Wireless Mouse", "price": 45.00, "product_type": "physical", "status": "Active", "dateAdded": "2026-04-02", "salesCount": 130, "url": "/products/17" },
    { "id": 18, "name": "Python Automation Masterclass", "price": 149.99, "product_type": "digital", "status": "Active", "dateAdded": "2026-03-25", "salesCount": 275, "url": "/products/18" },
    { "id": 19, "name": "Ultra-Wide Monitor Light Bar", "price": 65.00, "product_type": "physical", "status": "Active", "dateAdded": "2026-03-14", "salesCount": 190, "url": "/products/19" },
    { "id": 20, "name": "Figma Wireframing Kit", "price": 24.00, "product_type": "digital", "status": "Active", "dateAdded": "2026-03-01", "salesCount": 510, "url": "/products/20" },
    { "id": 21, "name": "Portable SSD 1TB", "price": 115.00, "product_type": "physical", "status": "Active", "dateAdded": "2026-02-18", "salesCount": 310, "url": "/products/21" },
    { "id": 22, "name": "Copywriting Swipe File Database", "price": 37.00, "product_type": "physical", "status": "Inactive", "dateAdded": "2026-02-10", "salesCount": 165, "url": "/products/22" },
    { "id": 23, "name": "Mechanical NumPad", "price": 32.50, "product_type": "physical", "status": "Active", "dateAdded": "2026-01-29", "salesCount": 78, "url": "/products/23" },
    { "id": 24, "name": "Social Media Content Planner", "price": 15.00, "product_type": "service", "status": "Active", "dateAdded": "2026-01-15", "salesCount": 940, "url": "/products/24" },
    { "id": 25, "name": "RGB Gaming Microphone", "price": 79.00, "product_type": "physical", "status": "Active", "dateAdded": "2026-01-05", "salesCount": 205, "url": "/products/25" }
]