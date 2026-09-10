from django.http import HttpRequest
from accounts.domains.exceptions import BusinessNotFoundError
from accounts.selectors import BusinessSelector
from products.serializers import CreateProductsSchema
from products.repository import ProductsRepo


class ProductsService:
    def __init__(self, *, request: HttpRequest) -> None:
        self.biz_selector = BusinessSelector()
        self.request = request
        
    def add_product(self, product_data: CreateProductsSchema):
        biz_obj = self.biz_selector.get_user_business(user_email=self.request.user.email, as_instance=True) # type: ignore
        if not biz_obj:
            raise BusinessNotFoundError()
        ProductsRepo(business_instance=biz_obj).create_product(data=product_data) # type:ignore
