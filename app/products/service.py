from django.http import HttpRequest
from accounts.domains.exceptions import BusinessNotFoundError
from accounts.selectors import BusinessSelector
from products.domain.exceptions import ProductNotFoundError, ProductAccessDeniedError
from products.selectors import ProductsSelector
from products.serializers import CreateProductsSchema, ModifyProductSchema
from products.repository import ProductsRepo


class ProductsService:
    def __init__(self, *, request: HttpRequest) -> None:
        self.biz_selector = BusinessSelector()
        self.product_selector = ProductsSelector()
        self.request = request
        
    def add_product(self, product_data: CreateProductsSchema):
        biz_obj = self.biz_selector.get_user_business(user_email=self.request.user.email, as_instance=True) # type: ignore
        if not biz_obj:
            raise BusinessNotFoundError()
        ProductsRepo(business_instance=biz_obj).get_or_create_product(data=product_data) # type:ignore
        
    def update_product(self, *, product_data:ModifyProductSchema):
        biz_obj = self.biz_selector.get_user_business(user_email=self.request.user.email, as_instance=True) # type: ignore
        product_obj = self.product_selector.get_product_with_business(p_ref=product_data.product_id)
        
        if not product_obj:
            raise ProductNotFoundError()
        if product_obj.business != biz_obj:
            raise ProductAccessDeniedError()
        
        ProductsRepo(business_instance=biz_obj).update_product_data(merchant=biz_obj, data=product_data) # type: ignore
