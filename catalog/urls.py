from django.urls import path
from . import views
from . import cart_views

urlpatterns = [
    # Main views
    path('showcase/', views.showcase, name='showcase'),
    path('products/', views.showcase, name='products'),
    path('mens/', views.mens_perfumes, name='mens_perfumes'),
    path('ladies/', views.ladies_perfumes, name='ladies_perfumes'),
    path('about/', views.about_us, name='about_us'),
    path('order/', views.contact_form, name='contact_form'),
    path('order-success/', views.order_success, name='order_success'),
    path('gallery/', views.gallery, name='gallery'),
    
    # Cart URLs
    path('cart/', cart_views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),  # JSON-based add to cart
    path('cart/add/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart_with_id'),  # URL-based add to cart
    path('cart/update/<int:item_id>/', cart_views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', cart_views.remove_cart_item, name='remove_cart_item'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
]
