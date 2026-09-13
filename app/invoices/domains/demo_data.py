from django.utils import timezone
from accounts.domains.entities import BusinessEntity
from customers.domains.entities import CustomerEntity
from invoices.domains.entity import InvoiceEntity, InvoiceItemEntity
from dataclasses import asdict
from typing import Any, Dict
from uuid import uuid4


def get_demo_invoice_context() -> Dict[str, Any]:
    """
    Generates structured mock data representing a real generated Invoice entity.
    """
    invoice = InvoiceEntity(
        ref="INV-2026-9042",
        status="PAID",
        created_at=timezone.now(),
        payment_method="Bank Transfer",
        channel="Instagram Direct",
        business=BusinessEntity(
            id=uuid4(),
            code="SIQ-BIZ-8820",
            name="Apex Digital Studio",
            address="124 Victoria Island Way, Suite 4B, Lagos, Nigeria",
            owner_email="billing@apexdigital.ng",
            business_type="online",
            phone_number="+234 803 000 0123",
            website_url="apexdigital.ng",
            instagram_url="apexdigital.ng",
            tiktok_url="apexdigital.hq"
        ),
        customer=CustomerEntity(
            id="CUST-1049", # type: ignore
            first_name="Sarah",
            last_name="Jenkins",
            email="sarah.j@workspace.com",
            phone_number="+2348034567890"
        ),
        items=[
            InvoiceItemEntity(
                id="PRD-001",
                name="Ergonomic Desk Setup & Monitor Arm",
                product_type="physical",
                quantity=2,
                unit_price=140000.00,
                total_price=280000.00
            ),
            InvoiceItemEntity(
                id="PRD-002",
                name="Design Systems & UI Kit (Commercial License)",
                product_type="digital",
                quantity=1,
                unit_price=45000.00,
                total_price=45000.00
            ),
            InvoiceItemEntity(
                id="PRD-003",
                name="Brand Identity Consultation",
                product_type="service",
                quantity=1,
                unit_price=75000.00,
                total_price=75000.00
            )
        ],
        sub_total=400000.00,
        discount_percentage=5.0,
        discount_amount=20000.00,
        tax_name="VAT",
        tax_percentage=7.5,
        tax_amount=28500.00,
        total_amount_paid=408500.00
    )
    return {"invoice": asdict(invoice)}
