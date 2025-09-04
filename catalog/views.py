from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import urllib.parse
import json
from .models import Product, Cart, CartItem


def showcase(request):
    """Showcase view with category-based filtering"""
    from .models import Product
    from django.db.models import Q
    
    # Start with all products
    products = Product.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        products = products.filter(category=category_filter)
    
    # Filter by price range
    price_range = request.GET.get('price_range')
    if price_range and price_range != 'all':
        if price_range == 'budget':
            products = products.filter(price__lte=1000)
        elif price_range == 'mid_range':
            products = products.filter(price__gt=1000, price__lte=3000)
        elif price_range == 'premium':
            products = products.filter(price__gt=3000)
    
    # Sort products
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:  # default to name
        products = products.order_by('name')
    
    # Get unique categories for filtering
    categories = Product.CATEGORY_CHOICES
    
    context = {
        'products': products,
        'search_query': search_query,
        'current_filters': {
            'category': category_filter,
            'price_range': price_range,
            'sort': sort_by,
        },
        'filter_options': {
            'categories': categories,
        },
        'total_products': products.count(),
    }
    
    return render(request, 'catalog/showcase.html', context)


def mens_perfumes(request):
    """A view to return the men's perfumes page"""
    return render(request, 'catalog/mens_perfumes.html')


def ladies_perfumes(request):
    """A view to return the ladies' perfumes page"""
    return render(request, 'catalog/ladies_perfumes.html')


def about_us(request):
    """A view to return the about us page"""
    return render(request, 'catalog/about_us.html')


def contact_form(request):
    """A view to handle custom perfume orders"""
    if request.method == 'POST':
        # Extract form data
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email', '')
        location = request.POST.get('location')
        perfume_name = request.POST.get('perfume_name')
        gender_category = request.POST.get('gender_category')
        scent_type = request.POST.get('scent_type', '')
        package_types = request.POST.getlist('package_type')
        ml_amount = request.POST.get('ml_amount', '')
        ml_quantity = request.POST.get('ml_quantity', '')
        package_size = request.POST.get('package_size', '')
        package_quantity = request.POST.get('package_quantity', '')
        special_requests = request.POST.get('special_requests', '')
        budget_range = request.POST.get('budget_range', '')
        delivery_urgency = request.POST.get('delivery_urgency', '')
        
        # Create professional WhatsApp message
        whatsapp_message = f"""LAMOUT PERFUMES - NEW ORDER REQUEST
========================================

CUSTOMER INFORMATION:
• Name: {customer_name}
• Phone: {phone_number}
• Email: {email if email else 'Not provided'}
• Location: {location}

PERFUME DETAILS:
• Product: {perfume_name}
• Category: {gender_category.title()}
• Fragrance Type: {scent_type.title() if scent_type else 'Not specified'}

ORDER SPECIFICATIONS:
• Package Type: {', '.join(package_types).title()}"""
        
        if 'ml' in package_types or 'both' in package_types:
            whatsapp_message += f"• ML Amount: {ml_amount}ml x {ml_quantity} bottles\n"
        
        whatsapp_message += f"""

PRICING & DELIVERY:
- Budget Range: {budget_range if budget_range else 'Not specified'}
- Delivery Urgency: {delivery_urgency if delivery_urgency else 'Standard'}

SPECIAL REQUESTS:
{special_requests if special_requests else 'None specified'}

NEXT STEPS:
- Contact customer to confirm order details
- Provide accurate pricing quote
- Arrange payment method
- Schedule delivery/pickup

Order Timestamp: {timezone.now().strftime('%d/%m/%Y at %H:%M')}
========================================

Thank you for choosing Lamout Perfumes!"""
        
        # URL encode the message for WhatsApp
        import urllib.parse
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/+254716301107?text={encoded_message}"
        
        messages.success(request, f'Thank you {customer_name}! Your order has been prepared. Click the WhatsApp button to send it to us.')
        
        # Store the WhatsApp URL in session to show it on the success page
        request.session['whatsapp_url'] = whatsapp_url
        request.session['customer_name'] = customer_name
        
        return HttpResponseRedirect(reverse('order_success'))
    
    return render(request, 'catalog/contact_form.html')


def order_success(request):
    """A view to show order success page"""
    whatsapp_url = request.session.get('whatsapp_url', '')
    customer_name = request.session.get('customer_name', '')
    
    context = {
        'whatsapp_url': whatsapp_url,
        'customer_name': customer_name,
    }
    
    return render(request, 'catalog/order_success.html', context)


def get_or_create_cart(request):
    """Helper function to get or create cart for current session"""
    if not request.session.session_key:
        request.session.create()
    
    cart, created = Cart.objects.get_or_create(
        session_key=request.session.session_key
    )
    return cart


@require_POST
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        is_custom_ml = data.get('is_custom_ml', False)
        custom_ml = float(data.get('custom_ml', 0)) if is_custom_ml else None
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'}, status=400)
            
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        
        # Calculate price based on quantity type
        if is_custom_ml and custom_ml:
            total_price = float(product.ml_price) * float(custom_ml)
            quantity = 1  # For custom ml, we treat it as 1 item with custom quantity
        else:
            total_price = float(product.price) * quantity
        
        # Create or update cart item
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            product=product,
            is_custom_ml=is_custom_ml,
            defaults={
                'quantity': quantity,
                'custom_ml': custom_ml,
                'total_price': total_price
            }
        )
        
        # Update cart totals
        cart.update_totals()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_total': cart.total_price,
            'cart_count': cart.item_count
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def checkout(request):
    """Checkout view to display the cart and handle order submission"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if request.method == 'POST':
        # Process the order
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        location = request.POST.get('location')
        special_requests = request.POST.get('special_requests', '')
        
        if not all([customer_name, phone_number, location]):
            messages.error(request, 'Please fill in all required fields')
            return redirect('catalog:checkout')
            
        # Prepare professional WhatsApp message
        whatsapp_message = f"""🌟 *LAMOUT PERFUME - NEW ORDER* 🌟

👤 *Customer Information:*
• Name: {customer_name}
• Phone: {phone_number}
• Email: {email if email else 'Not provided'}
• Location: {location}

🛍️ *Order Details:*"""
        
        total_amount = 0
        for item in cart_items:
            item_total = item.total_price
            total_amount += item_total
            product_info = f"{item.quantity}x {item.product.name}"
            if item.is_custom_ml and item.custom_ml:
                product_info += f" ({item.custom_ml}ml custom)"
            whatsapp_message += f"\n• {product_info} - *KSH {item_total:,.2f}*"
        
        whatsapp_message += f"""

💰 *TOTAL AMOUNT: KSH {total_amount:,.2f}*

📝 *Special Requests:*
{special_requests if special_requests else 'None'}

━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Order via: lamoutperfumes.pythonanywhere.com
⏰ Order Time: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Please confirm payment method and delivery details. Thank you for choosing Lamout Perfume! 🙏"""
        
        # URL encode the message for WhatsApp
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/254616301107?text={encoded_message}"
        
        # Store data for success page
        request.session['whatsapp_url'] = whatsapp_url
        request.session['customer_name'] = customer_name
        request.session['order_total'] = float(total_amount)
        
        # Clear the cart
        cart_items.delete()
        cart.update_totals()
        
        return redirect('catalog:checkout_success')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': cart.total_price if hasattr(cart, 'total_price') else 0,
    }
    return render(request, 'catalog/checkout.html', context)


def checkout_success(request):
    """Checkout success page"""
    whatsapp_url = request.session.get('whatsapp_url', '')
    customer_name = request.session.get('customer_name', '')
    order_total = request.session.get('order_total', 0)
    
    # Clear the session data after displaying it
    if 'whatsapp_url' in request.session:
        del request.session['whatsapp_url']
    if 'customer_name' in request.session:
        del request.session['customer_name']
    if 'order_total' in request.session:
        del request.session['order_total']
    
    context = {
        'whatsapp_url': whatsapp_url,
        'customer_name': customer_name,
        'order_total': order_total,
    }
    
    return render(request, 'catalog/checkout_success.html', context)


def gallery(request):
    """Gallery view to display all perfume images"""
    import os
    from django.conf import settings
    
    # Get all image files from media directory
    media_path = os.path.join(settings.MEDIA_ROOT)
    image_files = []
    
    if os.path.exists(media_path):
        for filename in os.listdir(media_path):
            if filename.lower().endswith(('.jpeg', '.jpg', '.png')) and filename.startswith('ER'):
                image_files.append(filename)
    
    # Sort the files
    image_files.sort()
    
    context = {
        'image_files': image_files
    }
    return render(request, 'catalog/gallery.html', context)
