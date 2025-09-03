from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(max_length=40, null=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class BusinessInfo(models.Model):
    """Store business information that can be edited from admin"""
    
    class Meta:
        verbose_name = "Business Information"
        verbose_name_plural = "Business Information"
    
    # Business Details
    business_name = models.CharField(max_length=100, default="Lamout Perfume")
    tagline = models.CharField(max_length=200, default="Discover exquisite fragrances that define your unique style")
    
    # Contact Information
    phone_number = models.CharField(max_length=20, default="+254616301107")
    email = models.EmailField(default="info@lamoutperfume.com")
    whatsapp_number = models.CharField(max_length=20, default="+254616301107")
    
    # Location
    address_line_1 = models.CharField(max_length=100, default="Neema House, First Floor")
    address_line_2 = models.CharField(max_length=100, default="Room 1007")
    city = models.CharField(max_length=50, default="Githunguri")
    county = models.CharField(max_length=50, default="Kiambu")
    country = models.CharField(max_length=50, default="Kenya")
    
    # Business Hours
    opening_hours = models.TextField(
        default="Monday - Saturday: 9:00 AM - 6:00 PM\nSunday: 10:00 AM - 4:00 PM"
    )
    
    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    
    # Website Content
    hero_title = models.CharField(max_length=100, default="Welcome to Lamout Perfume")
    hero_subtitle = models.CharField(max_length=200, default="Discover exquisite fragrances that define your unique style")
    about_us = models.TextField(
        default="We specialize in premium perfumes for men and women, offering both packaged bottles and custom ML measurements to suit your preferences."
    )
    
    # Discounts and Offers
    current_discount_percentage = models.PositiveIntegerField(default=0, help_text="Current site-wide discount %")
    discount_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Minimum amount for discount")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.business_name} - Business Info"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and BusinessInfo.objects.exists():
            raise ValueError("Only one BusinessInfo instance is allowed")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_info(cls):
        """Get the business info instance, create if doesn't exist"""
        info, created = cls.objects.get_or_create(pk=1)
        return info
