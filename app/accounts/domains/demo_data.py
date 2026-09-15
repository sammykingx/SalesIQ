from .entities import BusinessEntity
from uuid import uuid4

def demo_business_entity():
    return BusinessEntity(
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
    )