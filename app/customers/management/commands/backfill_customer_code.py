# customers/management/commands/backfill_customer_code.py
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

from customers.domains.customer_code import build_unique_customer_code
from customers.models import Customers


class Command(BaseCommand):
    help = (
        "Assign a code to every Customers row that has none. "
        "Existing codes are never changed. Safe to re-run."
    )

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=500)
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Report how many customers need a code, then exit without writing.",
        )

    def handle(self, *args, batch_size, dry_run, **options):
        rows_updated = 0
        missing = Q(code__isnull=True) | Q(code="")
        total = Customers.objects.filter(missing).count()
        self.stdout.write(f"{total} customers need a unique code")
        if dry_run or not total:
            return

        done, last_pk = 0, 0
        while True:
            # One short transaction per batch. select_for_update locks the batch rows, so a
            # concurrent save() can't assign a different code between our read and write.
            # Rows that got a code in the meantime no longer match `missing` once locked.
            with transaction.atomic():
                batch = list(
                    Customers.objects.select_for_update()
                    .filter(missing, pk__gt=last_pk)  # keyset paging: always terminates
                    .only("pk", "first_name", "last_name")
                    .order_by("pk")[:batch_size]
                )
                if not batch:
                    break
                for customer in batch:
                    customer.code = build_unique_customer_code(
                        f_name=customer.first_name,
                        l_name=customer.last_name,
                    )
                    self.stdout.write(self.style.SUCCESS(f"First name: {customer.first_name} last_name: {customer.last_name}, code: {customer.code}"))
                
                rows_updated = Customers.objects.bulk_update(batch, ["code"])

            last_pk = batch[-1].pk
            done += len(batch)
            self.stdout.write(f"{done}/{total}")

        remaining = Customers.objects.filter(missing).count()
        if remaining:
            raise CommandError(f"{remaining} customers still have no code; re-run the command")
        self.stdout.write(self.style.SUCCESS(f"{rows_updated} customers have a unique code, with {remaining} left out of {total}"))
        