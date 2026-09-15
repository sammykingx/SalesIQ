from django.utils import timezone
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict


def demo_invoice_data() -> Dict[str, Any]:
    """Returns a dict shaped to InvoiceDetailResponseSchema for testing/demo use."""
    return {
        "display_id": "INV-0001",
        "slug": "demo-invoice-inv-0001",
        "business": {
            "code": "BIZ001",
            "name": "Clarové Demo Store",
            "phone_number": "+2348000000000",
            "business_type": "Retail",
            "address": "12 Demo Street, Lagos",
            "instagram_url": "https://instagram.com/clarovedemo",
            "tiktok_url": None,
            "website_url": "https://clarovedemo.com",
        },
        "customer": {
            "first_name": "Ada",
            "last_name": "Obi",
            "email": "ada.obi@example.com",
            "phone_number": "+2348111111111",
        },
        "subtotal": Decimal("15000.00"),
        "discount_type": "PERCENTAGE",
        "discount_value": Decimal("0.05"),
        "discount_amount": Decimal("750.00"),
        "tax_name": "VAT",
        "tax_percentage": Decimal("7.50"),
        "tax_amount": Decimal("1068.75"),
        "total": Decimal("15318.75"),
        "currency": "NGN",
        "status": "PAID",
        "items": [
            {
                "product_name": "Ankara Fabric (6 yards)",
                "product_type": "Fabric",
                "unit_price": Decimal("5000.00"),
                "quantity": 2,
                "line_subtotal": Decimal("10000.00"),
            },
            {
                "product_name": "Custom Tailoring Fee",
                "product_type": "Service",
                "unit_price": Decimal("5000.00"),
                "quantity": 1,
                "line_subtotal": Decimal("5000.00"),
            },
        ],
        "created_at": datetime.now(timezone.utc),
    }
 