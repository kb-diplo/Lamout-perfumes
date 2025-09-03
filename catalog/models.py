from django.db import models
from django.contrib.sessions.models import Session


class Product(models.Model):
    """Model for perfume products"""
    CATEGORY_CHOICES = [
        ('mens', "Men's Collection"),
        ('ladies', "Ladies' Collection"),
        ('unisex', 'Unisex'),
        ('woody', 'Woody'),
        ('fresh', 'Fresh'),
        ('oriental', 'Oriental'),
        ('floral', 'Floral'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='unisex')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Price for one full package"
    )
    ml_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Price per ml (for custom quantities)"
    )
    stock_quantity = models.PositiveIntegerField(
        default=100, 
        help_text="Number of available full packages"
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.name
    
    def get_display_category(self):
        """Get the main display category for this product"""
        return self.category
    
    def get_price_range(self):
        """Get price range category for filtering"""
        if self.price <= 1000:
            return 'budget'
        elif self.price <= 3000:
            return 'mid_range'
        else:
            return 'premium'
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0


class Cart(models.Model):
    """Model for shopping cart"""
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id} - {self.session_key}"
    
    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    def update_totals(self):
        """Update the cart's total price and save"""
        self.save()


class CartItem(models.Model):
    """Model for items in the cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_custom_ml = models.BooleanField(default=False)
    custom_ml = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.is_custom_ml and self.custom_ml:
            return f"{self.custom_ml}ml {self.product.name}"
        return f"{self.quantity}x {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total price before saving
        if self.is_custom_ml and self.custom_ml:
            self.total_price = float(self.product.ml_price) * float(self.custom_ml)
        else:
            self.total_price = float(self.product.price) * int(self.quantity)
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('cart', 'product', 'is_custom_ml', 'custom_ml')
