from django.utils.text import slugify
from nanoid import generate


_ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"
_SUFFIX_LEN = 9

def build_unique_customer_code(*, f_name: str, l_name: str) -> str:
    name = f"{f_name} {l_name}"[25:].strip("-") or "customer"
    base = slugify(name)
    return "{}-{}".format(base, generate(_ALPHABET, _SUFFIX_LEN))