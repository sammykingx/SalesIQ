from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.urls import reverse
from urllib.parse import urlencode

from core.url_names import PRODUCTS
from products.models import Products
from products.domain.entities import ProductEntity
from products.domain.exceptions import ProductNotFoundError
from typing import List, Optional, Union, Dict, Any
from uuid import UUID


class ProductsSelector:
    def __init__(self) -> None:
        self.model = Products

    def _to_entity(self, product: Products) -> ProductEntity:
        """Helper method to map a Django model instance to a domain ProductEntity."""
        return ProductEntity(
            id=product.id,
            name=product.name,
            price=product.price,
            product_type=product.product_type,
            description=product.description,
            business_id=product.business_id, # type:ignore
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    def get_product(self, *, product_id: UUID, as_instance: bool = False) -> Union[Products, ProductEntity, None]:
        """
            Retrieves a single product by its UUID. 
            Returns a Django model instance if as_instance=True, otherwise returns a ProductEntity.
        """
        product = self.model.objects.filter(pk=product_id).first()
        if not product:
            return None

        if as_instance:
            return product
            
        return self._to_entity(product)
    
    def get_product_with_business(self, *, p_ref) -> Optional[Products]:
        """Fetches the product and optimizes the query by joining the business relation."""
        try:
            return self.model.objects.select_related("business").get(pk=p_ref)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None

    def get_business_products(self, *, business_id: UUID, as_instance: bool = False) -> Union[List[Products], List[Dict[str, Any]]]:
        """
            Retrieves all products for a specific business. 
            Annotates total sales and formats dates for the frontend list schema if not returning instances.
        """
        # Annotate total sales (assuming your sales/order relation is named 'sales' or 'order_items')
        queryset = self.model.objects.filter(business_id=business_id).annotate(
            total_sales=Count("line_items__invoice", distinct=True)
        ).order_by('-created_at')
        
        if not queryset:
            return []

        if as_instance:
            return list(queryset)

        return [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "product_type": product.product_type,
                "total_sales": getattr(product, 'total_sales', 0),
                "created_at": product.created_at.isoformat(),
                "url": f"{reverse(PRODUCTS.DETAIL)}?{urlencode({'p_ref': product.id})}"
            }
            for product in queryset
        ]
