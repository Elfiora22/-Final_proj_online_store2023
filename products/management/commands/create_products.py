from django.core.management.base import BaseCommand
from products.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("my 1st command")
        new_brand = Brand.objects.create(title="Superbrand")
        Product.objects.create(
            title="Good product",
            price=100,
            old_price=150,
            quantity= 15,
            brand = new_brand
        )
        Product.objects.create(
            title="bad product",
            price=13,
            old_price=14,
            quantity= 10,
            brand = new_brand
        )
        