from django.db import IntegrityError
from django.db.models import Model
from accounts.domains.entities import BusinessEntity
from accounts.models import Business
from invoices.models import Invoice, InvoiceLineItem
from invoices.domains.exceptions import InvoiceIdentifierCollisionError
from invoices.serializers import InvoiceLineItemSchema, CreateSalesInvoiceSchema
from decimal import Decimal
from nanoid import generate
import hashlib, string


INVOICE_ID_ALPHABET = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SLUG_ALPHABET = string.ascii_lowercase + string.digits

class InvoiceRepository:
    """ Handles all db writes to the invocie table
    """
    def __init__(self) -> None:
        self.inv_model = Invoice
        self.inv_line_item_model = InvoiceLineItem
        
    
    def _business_hash_segment(self, business_code: str, length: int = 4) -> str:
        """
            Deterministic 4-char segment derived from the business's own code.
            Same business always produces the same segment — but it's not just a
            visible slice of BIZ-XXXXXXXXXX, so it doesn't leak the business code.
        """
        digest = hashlib.sha256(business_code.encode()).hexdigest()
        n = int(digest, 16)
        base = len(INVOICE_ID_ALPHABET)
        chars = []
        for _ in range(length):
            n, rem = divmod(n, base)
            chars.append(INVOICE_ID_ALPHABET[rem])
        return "".join(chars)
    
    def generate_invoice_display_id(self, *, business:Business) -> str:
        """
            SIQ-INV-<business_hash>-<random>
            - business_hash: stable per business, ties every invoice visibly to one seller
            - random: independent 4-char draw per invoice — no sequence to enumerate
        """
        business_segment = self._business_hash_segment(business.code)
        for _ in range(10):
            random_segment = generate(INVOICE_ID_ALPHABET, 4)
            candidate = f"SIQ-INV-{business_segment}-{random_segment}"
            if not self.inv_model.objects.filter(display_id=candidate).exists():
                return candidate
        raise RuntimeError("Could not generate a unique invoice display_id after 10 attempts")
    
    def generate_invoice_slug(self, *, length: int = 34) -> str:
        """
            Public receipt URL token
        """
        for _ in range(10):
            candidate = generate(SLUG_ALPHABET, length)
            if not self.inv_model.objects.filter(slug=candidate).exists():
                return candidate
        raise RuntimeError("Could not generate a unique invoice slug after 10 attempts")

    def create_invoice_line_item(self, *, invoice_obj: Invoice, product_obj: Model, line_item:InvoiceLineItemSchema):
        return self.inv_line_item_model.objects.create(
            invoice=invoice_obj,
            product=product_obj,
            product_name=line_item.name,
            product_type=line_item.product_type,
            unit_price=line_item.price,
            quantity=line_item.quantity,
            line_subtotal=(line_item.price * line_item.quantity).quantize(Decimal("0.01"))
        )
        
    def create_invoice(self, *, business_instance: Business, customer_instance: Model, data: CreateSalesInvoiceSchema):
        for attempt in range(3):
            try:
                return self.inv_model.objects.create(
                    display_id=self.generate_invoice_display_id(business=business_instance),
                    slug=self.generate_invoice_slug(),
                    business=business_instance,
                    customer=customer_instance,
                    subtotal=data.sub_total,
                    discount_value=data.discount_percentage,
                    discount_amount=data.discount_amount,
                    tax_name=data.tax_name,
                    tax_percentage=data.tax_percentage,
                    tax_amount=data.tax_amount,
                    total=data.total_amount,
                )
                
            except IntegrityError as e:
                if attempt == 2:
                    raise InvoiceIdentifierCollisionError() from e
        raise InvoiceIdentifierCollisionError()
