from accounts.domains.entities import BusinessEntity
from invoices.models import Invoice, InvoiceLineItem
from nanoid import generate
import hashlib


INVOICE_ID_ALPHABET = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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
    
    def generate_invoice_display_id(self, business:BusinessEntity) -> str:
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

        
    