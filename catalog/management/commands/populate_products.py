from django.core.management.base import BaseCommand
from catalog.models import Product

class Command(BaseCommand):
    help = 'Populates the database with perfume products from the provided list.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate products...')

        ladies_perfumes = {
            'woody': [
                'Baccarat Rouge', 'Black opium', 'Good girl', 'Givenchy l\'interdit',
                'Decadence', 'Gucci guilty woman', 'Giorgio Armani my way'
            ],
            'floral': [
                'Riri by Rihanna', 'Gumdrop the beat', 'Gucci Flora', 'Escada Taj',
                'Prada candy', 'Kayalli Eden', 'Midnight Fantasy'
            ],
            'fresh': [
                'D&G light blue', 'Paris Hilton', 'Her Burberry', 'Chance chanel',
                'Marc jacobs', 'Versace bright crystal'
            ],
            'oriental': [
                'Libre Ysl', 'Delina exclusif', 'Yara', 'La vie Este belle',
                'Coco mademoiselle', 'Chanel no 5', 'Dior jadore'
            ]
        }

        mens_perfumes = {
            'woody': [
                'One million', 'Issey miyake', 'Tom Ford Oud', 'Hugo Boss man',
                'Guccr guilty woman', 'Polo red', 'Sauvagedior', 'Aqua di Gio'
            ],
            'oriental': [
                'Jimmy Choo', 'Dunhill Red desire', 'Creed Aventus', 'Bleu de Chanel',
                '212 vip black man', 'James bond', 'Invictus man', 'Allure home sport',
                'Azzaro most wanted', 'Polo black'
            ],
            'fresh': [
                'Stronger with you', 'D&G light blue', 'Invictus aqua', 'Prada ocean',
                'Burberry Brit', 'Gucci guilty', 'Aqua di gio'
            ]
        }

        # Add Ladies' Perfumes
        for scent_type, names in ladies_perfumes.items():
            for name in names:
                product, created = Product.objects.get_or_create(
                    name=name,
                    category='ladies',
                    defaults={
                        'price': 2500.00,
                        'ml_price': 30.00,
                        'stock_quantity': 50,
                        'description': f'{name} - A captivating fragrance for women. Scent profile: {scent_type}.'
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created ladies product: {name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Ladies product "{name}" already exists.'))

        # Add Men's Perfumes
        for scent_type, names in mens_perfumes.items():
            for name in names:
                # Correcting a typo from the image 'Guccr' -> 'Gucci'
                if name == 'Guccr guilty woman':
                    name = 'Gucci guilty woman'

                product, created = Product.objects.get_or_create(
                    name=name,
                    category='mens',
                    defaults={
                        'price': 2500.00,
                        'ml_price': 30.00,
                        'stock_quantity': 50,
                        'description': f'{name} - A powerful fragrance for men. Scent profile: {scent_type}.'
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created mens product: {name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Mens product "{name}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Finished populating products.'))
