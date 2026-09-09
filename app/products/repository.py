
from django.db import transaction, IntegrityError
from accounts.models import Business
from products.domain.exceptions import ProductAlreadyExistsError
from products.models import Products
from products.serializers import CreateProductsSchema


class ProductsRepo:
    def __init__(self, *, business_instance: Business) -> None:
        if not isinstance(business_instance, Business):
            raise ValueError("Initialize the products repo with an actual Businedd model instance/object")
        
        self.model = Products
        self.biz_obj = business_instance
    
    @transaction.atomic
    def create_product(self, *, data: CreateProductsSchema) -> Products:
        try:
            return self.model.objects.create(
                name=data.name,
                price=data.price,
                product_type=data.product_type,
                description=data.description,
                business=self.biz_obj,
            )
        except IntegrityError:
            raise ProductAlreadyExistsError(
                message=f"A product named '{data.name}' already exists for this business."
            )