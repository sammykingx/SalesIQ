from django.test import TestCase
from customers.domains.customer_code import build_unique_customer_code
import re

# Create your tests here.
def test_code_format_and_uniqueness():
    codes = {build_unique_customer_code(f_name="Ada", l_name="Obi") for _ in range(50_000)}
    assert len(codes) == 50_000
    assert all(re.fullmatch(r"ada-obi-[a-hjkmnp-z2-9]{9}", c) for c in codes)