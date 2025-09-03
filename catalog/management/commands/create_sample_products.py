from django.core.management.base import BaseCommand
from catalog.models import Product


class Command(BaseCommand):
    help = 'Create sample perfume products for testing'

    def handle(self, *args, **options):
        # Sample products data
        products_data = [
            {
                'name': 'Chanel No. 5',
                'description': 'The world\'s most iconic fragrance with notes of ylang-ylang, rose, and sandalwood.',
                'category': 'ladies',
                'price': 120.00,
                'ml_price': 2.50,
                'stock_quantity': 50,
                'is_featured': True
            },
            {
                'name': 'Dior Sauvage',
                'description': 'A fresh and woody fragrance with bergamot, pepper, and ambroxan.',
                'category': 'mens',
                'price': 95.00,
                'ml_price': 2.20,
                'stock_quantity': 75,
                'is_featured': True
            },
            {
                'name': 'Tom Ford Black Orchid',
                'description': 'A luxurious and sensual fragrance with black truffle, ylang-ylang, and dark chocolate.',
                'category': 'unisex',
                'price': 150.00,
                'ml_price': 3.00,
                'stock_quantity': 30,
                'is_featured': False
            },
            {
                'name': 'Versace Bright Crystal',
                'description': 'A fresh floral fragrance with pomegranate, peony, and musk.',
                'category': 'ladies',
                'price': 80.00,
                'ml_price': 1.80,
                'stock_quantity': 60,
                'is_featured': False
            },
            {
                'name': 'Acqua di Gio',
                'description': 'A fresh aquatic fragrance with marine notes, bergamot, and white musk.',
                'category': 'mens',
                'price': 85.00,
                'ml_price': 1.90,
                'stock_quantity': 45,
                'is_featured': True
            },
            {
                'name': 'Yves Saint Laurent Black Opium',
                'description': 'A seductive fragrance with coffee, vanilla, and white flowers.',
                'category': 'ladies',
                'price': 110.00,
                'ml_price': 2.40,
                'stock_quantity': 40,
                'is_featured': False
            },
            {
                'name': 'Creed Aventus',
                'description': 'A sophisticated blend of pineapple, birch, and musk.',
                'category': 'mens',
                'price': 300.00,
                'ml_price': 6.00,
                'stock_quantity': 20,
                'is_featured': True
            },
            {
                'name': 'Maison Margiela REPLICA Beach Walk',
                'description': 'A sunny fragrance capturing the essence of a summer beach day.',
                'category': 'unisex',
                'price': 125.00,
                'ml_price': 2.60,
                'stock_quantity': 35,
                'is_featured': False
            },
            {
                'name': 'Dolce & Gabbana Light Blue',
                'description': 'A fresh Mediterranean fragrance with lemon, apple, and cedar.',
                'category': 'ladies',
                'price': 75.00,
                'ml_price': 1.70,
                'stock_quantity': 55,
                'is_featured': False
            },
            {
                'name': 'Hugo Boss Bottled',
                'description': 'A modern masculine fragrance with apple, cinnamon, and sandalwood.',
                'category': 'mens',
                'price': 70.00,
                'ml_price': 1.60,
                'stock_quantity': 65,
                'is_featured': False
            }
        ]

        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new products!')
        )
