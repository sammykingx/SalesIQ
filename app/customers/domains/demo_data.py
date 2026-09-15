from .entities import CustomerEntity

def demo_customer_entity() -> CustomerEntity:
    return CustomerEntity(
        id=3,
        first_name="Sarah",
        last_name="Jenkins",
        email="sarah.j@workspace.com",
        phone_number="+2348034567890"
    )