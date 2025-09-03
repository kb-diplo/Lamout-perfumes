from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Product, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'ml_price', 'stock_quantity', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'ml_price', 'stock_quantity', 'is_featured')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'is_featured')
        }),
        ('Categorization', {
            'fields': ('category',),
            'description': 'Organize products by category'
        }),
        ('Pricing', {
            'fields': ('price', 'ml_price'),
            'description': 'Set both full package price and price per ml for custom quantities'
        }),
        ('Inventory', {
            'fields': ('stock_quantity',),
            'description': 'Track inventory for full packages only'
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"
    
    actions = ['mark_as_featured', 'mark_as_not_featured']
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products marked as featured.')
    mark_as_featured.short_description = "Mark selected products as featured"
    
    def mark_as_not_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products removed from featured.')
    mark_as_not_featured.short_description = "Remove featured status"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'is_custom_ml', 'custom_ml', 'total_price', 'added_at')
    fields = ('product', 'quantity', 'is_custom_ml', 'custom_ml', 'total_price')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at', 'total_items', 'total_value', 'view_items')
    list_filter = ('created_at',)
    search_fields = ('session_key',)
    readonly_fields = ('session_key', 'created_at', 'total_items', 'total_value')
    ordering = ('-created_at',)
    
    inlines = [CartItemInline]
    
    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = "Items Count"
    
    def total_value(self, obj):
        return f"Ksh {obj.get_total():.2f}"
    total_value.short_description = "Cart Value"
    
    def view_items(self, obj):
        items = obj.items.select_related('product').all()
        if items.exists():
            item_display = ""
            for item in items[:3]:  # Show first 3 items
                item_display += f"{item.quantity}x {item.product.name}<br>"
            if items.count() > 3:
                item_display += f"<br>... and {items.count() - 3} more"
            return mark_safe(item_display)
        return "Empty Cart"
    view_items.short_description = "Cart Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'is_custom_ml', 'custom_ml', 'total_price', 'added_at')
    list_filter = ('added_at', 'is_custom_ml')
    search_fields = ('product__name', 'cart__session_key')
    readonly_fields = ('added_at', 'total_price')
    ordering = ('-added_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'cart')


# Custom Admin Site Configuration
admin.site.site_header = "Lamout Perfume Administration"
admin.site.site_title = "Lamout Perfume Admin"
admin.site.index_title = "Welcome to Lamout Perfume Administration"
