from django import template

register = template.Library()


@register.filter
def compact_number(value):
    """1234 -> '1.2K', 1000000 -> '1M', 999 -> '999' (unchanged below 1000)."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    abs_value = abs(value)
    sign = "-" if value < 0 else ""

    if abs_value < 1_000:
        return f"{sign}{int(abs_value)}"
    if abs_value < 1_000_000:
        formatted = f"{abs_value / 1_000:.1f}".rstrip("0").rstrip(".")
        return f"{sign}{formatted}K"
    if abs_value < 1_000_000_000:
        formatted = f"{abs_value / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"{sign}{formatted}M"
    formatted = f"{abs_value / 1_000_000_000:.1f}".rstrip("0").rstrip(".")
    return f"{sign}{formatted}B"