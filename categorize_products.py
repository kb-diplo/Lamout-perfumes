#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lamoutperfumes.settings')
django.setup()

from catalog.models import Product

# Define fragrance categorization based on typical perfume profiles
FRAGRANCE_CATEGORIES = {
    # Woody fragrances
    'woody': [
        'Tom Ford Oud', 'Creed Aventus', 'Sauvagedior', 'Hugo Boss man',
        'Dunhill Red desire', 'Polo black', 'Azzaro most wanted'
    ],
    
    # Fresh fragrances  
    'fresh': [
        'Aqua di gio', 'D&G light blue', 'Prada ocean', 'Invictus aqua',
        'Allure home sport', 'Issey miyake', 'Versace bright crystal',
        'D&G light blue'
    ],
    
    # Oriental fragrances
    'oriental': [
        'One million', 'Stronger with you', '212 vip black man', 'James bond',
        'Yara', 'Black opium', 'Baccarat Rouge', 'Decadence'
    ],
    
    # Floral fragrances
    'floral': [
        'Dior jadore', 'Chanel no 5', 'Coco mademoiselle', 'La vie Este belle',
        'Delina exclusif', 'Libre Ysl', 'Chance chanel', 'Her Burberry',
        'Gucci Flora', 'Givenchy l\'interdit', 'Good girl', 'Giorgio Armani my way'
    ]
}

def categorize_products():
    """Categorize products based on fragrance profiles"""
    print("=== CATEGORIZING PRODUCTS ===")
    
    for category, product_names in FRAGRANCE_CATEGORIES.items():
        for product_name in product_names:
            # Try to find product by exact name or partial match
            products = Product.objects.filter(name__icontains=product_name.split()[0])
            
            for product in products:
                if any(word.lower() in product.name.lower() for word in product_name.split()):
                    old_category = product.category
                    product.category = category
                    product.save()
                    print(f"Updated: {product.name} from '{old_category}' to '{category}'")
                    break
    
    print("\n=== FINAL CATEGORY COUNTS ===")
    for choice in Product.CATEGORY_CHOICES:
        count = Product.objects.filter(category=choice[0]).count()
        print(f"{choice[0]}: {choice[1]} - {count} products")

if __name__ == "__main__":
    categorize_products()
