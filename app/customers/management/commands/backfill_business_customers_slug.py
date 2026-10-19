# customers/management/commands/backfill_business_customers_slug.py

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

from customers.domains.customer_code import build_business_customer_slug
from customers.models import BusinessCustomers


class Command(BaseCommand):
    help = "Backfill BusinessCustomers.slug for rows that have none. Safe to re-run."

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=500)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, batch_size, dry_run, **options):
        missing = Q(slug__isnull=True) | Q(slug="")
        total = BusinessCustomers.objects.filter(missing).count()
        self.stdout.write(f"{total} business customers need a slug")
        if dry_run or not total:
            return

        done, last_pk = 0, 0
        while True:
            # keyset pagination on pk: always terminates, even if a row fails to update
            batch = list(
                BusinessCustomers.objects.filter(missing, pk__gt=last_pk)
                .select_related("client")
                .order_by("pk")[:batch_size]
            )
            if not batch:
                break

            for bc in batch:
                name = bc.display_name or f"{bc.client.first_name} {bc.client.last_name}"
                bc.slug = build_business_customer_slug(name)

            with transaction.atomic():
                BusinessCustomers.objects.bulk_update(batch, ["slug"])

            last_pk = batch[-1].pk
            done += len(batch)
            self.stdout.write(f"{done}/{total}")

        remaining = BusinessCustomers.objects.filter(missing).count()
        if remaining:
            raise CommandError(f"{remaining} rows still have no slug; re-run the command")
        self.stdout.write(self.style.SUCCESS("All business customers have a slug"))
