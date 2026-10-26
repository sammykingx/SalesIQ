
from django.db import transaction, IntegrityError
from django.utils import timezone
from accounts.models import Business
from products.domain.exceptions import ProductAlreadyExistsError, ProductNotFoundError
from products.models import Products
from products.serializers import CreateProductsSchema, ModifyProductSchema


class ProductsRepo:
    """
    Repository class responsible for managing database operations for products 
    scoped to a specific Business tenant.

    Enforces tenant isolation by ensuring all lookups and creations are tied 
    directly to the initialized business instance.
    """
    def __init__(self, *, business_instance: Business) -> None:
        if not isinstance(business_instance, Business):
            raise ValueError("Initialize the products repo with an actual Businedd model instance/object")
        
        self.model = Products
        self.biz_obj = business_instance

    def _find_existing_business_product(self, *, product_id) -> Products | None:
        """
        Safely retrieves an existing product by its unique identifier, strictly 
        scoped to the current business tenant.

        Args:
            product_id: The primary key (UUID or int) of the product being searched for.

        Returns:
            Optional[Products]: The matching product instance if found; otherwise, None.
        """
        return self.model.objects.filter(
            business=self.biz_obj,
            id=product_id
        ).first()
     
    def _create_business_product(self, data: CreateProductsSchema) -> Products:
        """
        Provisions and saves a new product record linked to the current business tenant.

        Args:
            data (CreateProductsSchema): The schema payload containing the product's 
                name, price, product_type, and optional description.

        Returns:
            Products: The newly created product model instance.

        Raises:
            ProductAlreadyExistsError: If a database IntegrityError occurs (typically 
                triggered if a product with the same name already exists for this business).
        """
        try:
            return self.model.objects.create(
                business=self.biz_obj,
                name=data.name,
                price=data.price,
                product_type=data.product_type,
                description=data.description,
            )
        except IntegrityError:
            raise ProductAlreadyExistsError(
                message=f"A product named '{data.name}' already exists in your products catalogue."
            )

    def get_or_create_product(self, *, product_id, data: CreateProductsSchema) -> Products:
        """
        Resolves a product during invoice creation or catalog management using a 
        conditional routing strategy:

        1. **Existing Product Flow:** If a truthy `product_id` is supplied, it delegates 
           to an ID-based lookup within the current business scope.
        2. **On-the-Fly Creation Flow:** If `product_id` is missing/None, it executes 
           an atomic transaction block to create a brand-new product using the provided 
           schema data.

        Args:
            product_id: The unique identifier of the product (if it already exists).
            data (CreateProductsSchema): The product payload data used as a fallback 
                for creation if no ID is present.

        Returns:
            Products: The retrieved or newly provisioned product model instance.
        """
        if product_id:
            return self._find_existing_business_product(product_id=product_id) # type: ignore
        
        with transaction.atomic():
            return self._create_business_product(data=data)
            
    def update_product_data(self, *, merchant:Business, data: ModifyProductSchema):
        return (
            self.model.objects
            .filter(pk=data.product_id, business=merchant)
            .update(
               name=data.name,
               price=data.price,
               product_type=data.product_type,
               description=data.description,
               updated_at=timezone.now()
            )
        )
        
    def delete_product(self, *, product_id) -> None:
        """
        Deletes a specific product from the business's product catalogue.

        Strictly enforces tenant isolation by ensuring the product belongs 
        to the current business instance before deletion. If the product cannot 
        be found or does not belong to this business, a `ProductNotFoundError` is raised.

        Args:
            product_id: The unique primary identifier (UUID or int) of the product to delete.

        Raises:
            ProductNotFoundError: If no matching product exists for this business tenant.
        """
        product = self._find_existing_business_product(product_id=product_id)
        
        if product is None:
            raise ProductNotFoundError(
                message=f"The product you are trying to delete does not exist in your catalogue."
            )
            
        product.delete()
        