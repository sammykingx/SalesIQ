from django.utils.text import slugify
from nanoid import generate


_ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"
_SUFFIX_LEN = 10

def build_unique_customer_code(*, f_name: str, l_name: str) -> str:
    first_name, last_name = f_name.strip("-"), l_name.strip("-")
    name = f"{first_name}-{last_name}"[:30] or "customer"
    base = slugify(name)
    return "{}-{}".format(base, generate(_ALPHABET, _SUFFIX_LEN))

def build_business_customer_slug(name: str) -> str:
    base = slugify(name)[:25].strip("-") or "client"
    return f"{base}-{generate(_ALPHABET, 15)}"
