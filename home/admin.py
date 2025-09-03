from django.contrib import admin
from .models import Subscriber, BusinessInfo


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_date")
    list_filter = ("subscribed_date",)
    search_fields = ("email",)
    ordering = ("-subscribed_date",)


@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Business Details', {
            'fields': ('business_name', 'tagline', 'about_us')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'whatsapp_number')
        }),
        ('Location', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'county', 'country')
        }),
        ('Business Hours', {
            'fields': ('opening_hours',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Website Content', {
            'fields': ('hero_title', 'hero_subtitle')
        }),
        ('Discounts & Offers', {
            'fields': ('current_discount_percentage', 'discount_threshold')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not BusinessInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
