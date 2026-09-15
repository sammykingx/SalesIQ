from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List


def demo_invoice_data() -> List[Dict[str, Any]]:
    """Returns a dict shaped to InvoiceDetailResponseSchema for testing/demo use."""
    return [
        {
            'display_id': 'SIQ-INV-4ZHG-7KVI',
            'created_at': datetime(2026, 9, 15, 3, 14, 42, 669114, tzinfo=timezone.utc),
            'customer': {'first_name': 'Kol', 'last_name': 'Mickeal', 'email': 'johmik@example.com', 'phone_number': '12345679809'},
            'status': 'paid',
            'total': Decimal('63375.00'),
            'url': '/invoices/r/8tpgybw9qak8i7eexy6w5hb2giho9l8t0x/'
        },
        {
            'display_id': 'SIQ-INV-9LMN-2XPQ',
            'created_at': datetime(2026, 9, 14, 12, 30, 15, 123456, tzinfo=timezone.utc),
            'customer': {'first_name': 'Sarah', 'last_name': 'Jenkins', 'email': 'sarah.j@example.com', 'phone_number': '55501928374'},
            'status': 'pending',
            'total': Decimal('1250.50'),
            'url': '/invoices/r/3k987asdfghjklqwertyuiopzxcvbnm12/'
        },
        {
            'display_id': 'SIQ-INV-3RST-8WXY',
            'created_at': datetime(2026, 9, 13, 15, 45, 10, 987654, tzinfo=timezone.utc),
            'customer': {'first_name': 'Marcus', 'last_name': 'Aurelius', 'email': 'm.aurelius@rome.gov', 'phone_number': '98765432100'},
            'status': 'paid',
            'total': Decimal('14200.00'),
            'url': '/invoices/r/9plokmijnbuhvygctfxrdeswaq123456/'
        },
        {
            'display_id': 'SIQ-INV-5BVC-1JKL',
            'created_at': datetime(2026, 9, 12, 8, 11, 55, 432109, tzinfo=timezone.utc),
            'customer': {'first_name': 'Elena', 'last_name': 'Gilbert', 'email': 'elena@mystic.falls', 'phone_number': '44455566677'},
            'status': 'overdue',
            'total': Decimal('450.75'),
            'url': '/invoices/r/5rfvgy7ujmki9olp0qazxswedcvfrtgb/'
        },
        {
            'display_id': 'SIQ-INV-7HGF-4EDC',
            'created_at': datetime(2026, 9, 11, 18, 22, 33, 112233, tzinfo=timezone.utc),
            'customer': {'first_name': 'Damon', 'last_name': 'Salvatore', 'email': 'damon@salvatore.com', 'phone_number': '11122233344'},
            'status': 'paid',
            'total': Decimal('8900.00'),
            'url': '/invoices/r/2wsxdr5ftgyhuji9kolp0okmijnuhbyg/'
        },
        {
            'display_id': 'SIQ-INV-2QAZ-6YHN',
            'created_at': datetime(2026, 9, 10, 9, 5, 0, 554433, tzinfo=timezone.utc),
            'customer': {'first_name': 'Bonnie', 'last_name': 'Bennett', 'email': 'bonnie@witches.net', 'phone_number': '99988877766'},
            'status': 'draft',
            'total': Decimal('320.00'),
            'url': '/invoices/r/7ujmki9olp0qazxswedcvfrtgbnhyujmi/'
        },
        {
            'display_id': 'SIQ-INV-8XSW-3UJM',
            'created_at': datetime(2026, 9, 9, 14, 19, 44, 778899, tzinfo=timezone.utc),
            'customer': {'first_name': 'Stefan', 'last_name': 'Salvatore', 'email': 'stefan@ripper.org', 'phone_number': '22233344455'},
            'status': 'pending',
            'total': Decimal('1299.99'),
            'url': '/invoices/r/4edcrfvgy7ujmki9olp0qazxswedcvfrt/'
        },
        {
            'display_id': 'SIQ-INV-1POI-9IKL',
            'created_at': datetime(2026, 9, 8, 11, 50, 12, 334455, tzinfo=timezone.utc),
            'customer': {'first_name': 'Caroline', 'last_name': 'Forbes', 'email': 'caroline@forbespr.com', 'phone_number': '33344455566'},
            'status': 'paid',
            'total': Decimal('5400.25'),
            'url': '/invoices/r/6yhnmju7kiolp0qazxswedcvfrtgbnhyu/'
        },
        {
            'display_id': 'SIQ-INV-6OKM-2YHN',
            'created_at': datetime(2026, 9, 7, 16, 40, 22, 667788, tzinfo=timezone.utc),
            'customer': {'first_name': 'Matt', 'last_name': 'Donovan', 'email': 'matt@sheriff.gov', 'phone_number': '77766655544'},
            'status': 'overdue',
            'total': Decimal('150.00'),
            'url': '/invoices/r/8ikolp0qazxswedcvfrtgbnhyujmki9o/'
        },
        {
            'display_id': 'SIQ-INV-4UJM-5TGB',
            'created_at': datetime(2026, 9, 6, 10, 15, 30, 990011, tzinfo=timezone.utc),
            'customer': {'first_name': 'Tyler', 'last_name': 'Lockwood', 'email': 'tyler@pack.net', 'phone_number': '88877766655'},
            'status': 'paid',
            'total': Decimal('12300.50'),
            'url': '/invoices/r/1qazxswedcvfrtgbnhyujmki9olp0qaz/'
        },
        {
            'display_id': 'SIQ-INV-9RFV-7EDC',
            'created_at': datetime(2026, 9, 5, 13, 25, 18, 223344, tzinfo=timezone.utc),
            'customer': {'first_name': 'Alaric', 'last_name': 'Saltzman', 'email': 'alaric@history.edu', 'phone_number': '55544433322'},
            'status': 'pending',
            'total': Decimal('780.00'),
            'url': '/invoices/r/9olp0qazxswedcvfrtgbnhyujmki9olp/'
        },
        {
            'display_id': 'SIQ-INV-2WSX-8RFV',
            'created_at': datetime(2026, 9, 4, 15, 10, 50, 445566, tzinfo=timezone.utc),
            'customer': {'first_name': 'Klaus', 'last_name': 'Mikaelson', 'email': 'klaus@hybrids.org', 'phone_number': '12312312312'},
            'status': 'paid',
            'total': Decimal('99999.99'),
            'url': '/invoices/r/3edcvfrtgbnhyujmki9olp0qazxswedc/'
        },
        {
            'display_id': 'SIQ-INV-3EDC-1WSX',
            'created_at': datetime(2026, 9, 3, 9, 0, 40, 778811, tzinfo=timezone.utc),
            'customer': {'first_name': 'Elijah', 'last_name': 'Mikaelson', 'email': 'elijah@nobility.co', 'phone_number': '32132132132'},
            'status': 'paid',
            'total': Decimal('45000.00'),
            'url': '/invoices/r/5tgbnhyujmki9olp0qazxswedcvfrtgb/'
        },
        {
            'display_id': 'SIQ-INV-5TGB-6YHN',
            'created_at': datetime(2026, 9, 2, 17, 33, 21, 332211, tzinfo=timezone.utc),
            'customer': {'first_name': 'Rebekah', 'last_name': 'Mikaelson', 'email': 'rebekah@original.com', 'phone_number': '45645645645'},
            'status': 'draft',
            'total': Decimal('2350.00'),
            'url': '/invoices/r/7ujmki9olp0qazxswedcvfrtgbnhyujm/'
        },
        {
            'display_id': 'SIQ-INV-7YHN-9UJM',
            'created_at': datetime(2026, 9, 1, 14, 12, 19, 889900, tzinfo=timezone.utc),
            'customer': {'first_name': 'Hayley', 'last_name': 'Marshall', 'email': 'hayley@crescent.org', 'phone_number': '78978978978'},
            'status': 'overdue',
            'total': Decimal('3400.00'),
            'url': '/invoices/r/2wsxdr5ftgyhuji9kolp0okmijnuhby/'
        },
        {
            'display_id': 'SIQ-INV-8IKL-3OPP',
            'created_at': datetime(2026, 8, 31, 11, 45, 0, 112244, tzinfo=timezone.utc),
            'customer': {'first_name': 'Freya', 'last_name': 'Mikaelson', 'email': 'freya@magic.runes', 'phone_number': '65465465465'},
            'status': 'paid',
            'total': Decimal('18900.50'),
            'url': '/invoices/r/4edcrfvgy7ujmki9olp0qazxswedc/'
        },
        {
            'display_id': 'SIQ-INV-1QAZ-2WSX',
            'created_at': datetime(2026, 8, 30, 8, 20, 11, 556677, tzinfo=timezone.utc),
            'customer': {'first_name': 'Marcel', 'last_name': 'Gerard', 'email': 'marcel@garden.com', 'phone_number': '98798798798'},
            'status': 'pending',
            'total': Decimal('7500.00'),
            'url': '/invoices/r/6yhnmju7kiolp0qazxswedcvfrtgbnhy/'
        },
        {
            'display_id': 'SIQ-INV-6RFV-4EDC',
            'created_at': datetime(2026, 8, 29, 16, 55, 30, 998877, tzinfo=timezone.utc),
            'customer': {'first_name': 'Vincent', 'last_name': 'Griffith', 'email': 'vincent@regents.org', 'phone_number': '14725836900'},
            'status': 'paid',
            'total': Decimal('2100.00'),
            'url': '/invoices/r/8ikolp0qazxswedcvfrtgbnhyujmki9/'
        },
        {
            'display_id': 'SIQ-INV-9UJM-5TGB',
            'created_at': datetime(2026, 8, 28, 12, 10, 45, 221144, tzinfo=timezone.utc),
            'customer': {'first_name': 'Josh', 'last_name': 'Rosza', 'email': 'josh@vampire.net', 'phone_number': '36925814700'},
            'status': 'draft',
            'total': Decimal('450.00'),
            'url': '/invoices/r/1qazxswedcvfrtgbnhyujmki9olp0q/'
        }
    ]
 