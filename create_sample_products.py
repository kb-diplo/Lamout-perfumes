#!/usr/bin/env python
"""
Script to create sample perfume products for Lamout Perfume store
Run this in PythonAnywhere: python create_sample_products.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lamoutperfumes.settings')
django.setup()

from catalog.models import Product

def create_products():
    """Create sample perfume products"""
    
    products_data = [
        # Men's Collection
        {"name": "Bleu de Chanel", "price": 4500, "category": "mens", "description": "Fresh and woody fragrance"},
        {"name": "Dior Sauvage", "price": 4200, "category": "mens", "description": "Wild and fresh scent"},
        {"name": "Tom Ford Oud Wood", "price": 6500, "category": "woody", "description": "Luxurious woody fragrance"},
        {"name": "Creed Aventus", "price": 8500, "category": "mens", "description": "Bold and confident scent"},
        {"name": "Giorgio Armani Acqua di Gio", "price": 3800, "category": "fresh", "description": "Fresh aquatic fragrance"},
        
        # Ladies' Collection
        {"name": "Chanel No. 5", "price": 5500, "category": "ladies", "description": "Iconic floral fragrance"},
        {"name": "Miss Dior", "price": 4800, "category": "floral", "description": "Elegant floral bouquet"},
        {"name": "Yves Saint Laurent Black Opium", "price": 4300, "category": "oriental", "description": "Addictive coffee and vanilla"},
        {"name": "Lancôme La Vie Est Belle", "price": 4600, "category": "ladies", "description": "Sweet and sophisticated"},
        {"name": "Viktor & Rolf Flowerbomb", "price": 4900, "category": "floral", "description": "Explosive floral fragrance"},
        
        # Unisex Collection
        {"name": "Le Labo Santal 33", "price": 7200, "category": "unisex", "description": "Creamy sandalwood scent"},
        {"name": "Byredo Gypsy Water", "price": 6800, "category": "unisex", "description": "Fresh and woody"},
        {"name": "Maison Margiela REPLICA Jazz Club", "price": 5200, "category": "unisex", "description": "Warm and smoky"},
        
        # Woody Collection
        {"name": "Hermès Terre d'Hermès", "price": 4700, "category": "woody", "description": "Earthy and mineral"},
        {"name": "Prada Luna Rossa", "price": 3900, "category": "woody", "description": "Modern woody fragrance"},
        
        # Fresh Collection
        {"name": "Dolce & Gabbana Light Blue", "price": 3500, "category": "fresh", "description": "Mediterranean freshness"},
        {"name": "Versace Dylan Blue", "price": 3200, "category": "fresh", "description": "Aquatic and citrusy"},
        
        # Oriental Collection
        {"name": "Thierry Mugler Angel", "price": 4400, "category": "oriental", "description": "Sweet and gourmand"},
        {"name": "Guerlain Shalimar", "price": 5800, "category": "oriental", "description": "Classic oriental fragrance"},
        
        # Floral Collection
        {"name": "Marc Jacobs Daisy", "price": 3600, "category": "floral", "description": "Fresh and feminine"},
        {"name": "Estée Lauder Beautiful", "price": 4100, "category": "floral", "description": "Romantic floral bouquet"},
    ]
    
    created_count = 0
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data["name"],
            defaults={
                'price': product_data["price"],
                'category': product_data["category"],
                'description': product_data["description"],
                'stock_quantity': 50,  # Default stock
                'is_available': True,
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created: {product.name} - {product.get_category_display()}")
        else:
            print(f"- Exists: {product.name}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Created {created_count} new products")
    print(f"Total products in database: {Product.objects.count()}")
    
    # Show category counts
    print(f"\n=== CATEGORY COUNTS ===")
    for category_code, category_name in Product.CATEGORY_CHOICES:
        count = Product.objects.filter(category=category_code).count()
        print(f"{category_code}: {category_name} - {count} products")

if __name__ == "__main__":
    print("=== CREATING SAMPLE PRODUCTS ===")
    create_products()
    print("=== DONE ===")
