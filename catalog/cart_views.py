from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.db.models import F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce
from decimal import Decimal
import json

from .models import Product, Cart, CartItem

def view_cart(request):
    """View the shopping cart"""
    cart = get_or_create_cart(request)
    
    # Annotate cart items with their total price
    cart_items = cart.items.select_related('product').annotate(
        item_total=ExpressionWrapper(
            Coalesce(F('custom_ml'), 0) * F('product__ml_price') + 
            Coalesce(F('quantity'), 0) * F('product__price'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )
    
    # Calculate cart totals
    cart_total = sum(item.item_total for item in cart_items)
    
    context = {
        'cart': {
            'total_price': cart_total,
            'total_items': cart.item_count
        },
        'cart_items': cart_items,
    }
    return render(request, 'catalog/cart.html', context)

@require_POST
def add_to_cart(request, product_id):
    """Add a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    try:
        data = json.loads(request.body)
        is_custom_ml = data.get('is_custom_ml', False)
        custom_ml = Decimal(str(data.get('custom_ml', 0))) if is_custom_ml else None
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)
    
    with transaction.atomic():
        # For custom ml quantities
        if is_custom_ml and custom_ml and custom_ml > 0:
            # Ensure we don't exceed available stock (convert ml to equivalent packages)
            ml_per_package = 100  # Assuming standard package size is 100ml
            equivalent_packages = (custom_ml / Decimal(ml_per_package)).quantize(Decimal('0.01'))
            
            if equivalent_packages > product.stock_quantity:
                return JsonResponse({
                    'success': False,
                    'error': f'Not enough stock. Only {product.stock_quantity} packages available.'
                }, status=400)
            
            # Create new cart item for custom ml
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                is_custom_ml=True,
                custom_ml=custom_ml,
                quantity=1  # Quantity is always 1 for custom ml items
            )
            message = f"Added {custom_ml}ml of {product.name} to your cart."
        
        # For full packages
        else:
            if product.stock_quantity < 1:
                return JsonResponse({
                    'success': False,
                    'error': 'This product is out of stock.'
                }, status=400)
            
            # Try to get existing cart item for this product (full package only)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                is_custom_ml=False,
                defaults={'quantity': 1}
            )
            
            if not created:
                if cart_item.quantity >= product.stock_quantity:
                    return JsonResponse({
                        'success': False,
                        'error': 'Not enough stock available.'
                    }, status=400)
                cart_item.quantity += 1
                cart_item.save()
            
            message = f"Added {product.name} to your cart."
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.item_count,
            'message': message
        })
    
    messages.success(request, message)
    return redirect('view_cart')

@require_POST
def update_cart_item(request, item_id):
    """Update quantity for a cart item"""
    try:
        cart_item = CartItem.objects.select_related('cart', 'product').get(
            id=item_id, 
            cart__session_key=request.session.session_key
        )
        
        data = json.loads(request.body)
        
        with transaction.atomic():
            # Update quantity for full packages
            if 'quantity' in data and not cart_item.is_custom_ml:
                quantity = int(data['quantity'])
                if quantity > cart_item.product.stock_quantity:
                    return JsonResponse({
                        'success': False, 
                        'error': f'Only {cart_item.product.stock_quantity} available in stock.'
                    }, status=400)
                
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            
            # Update custom ml amount
            elif 'custom_ml' in data and cart_item.is_custom_ml:
                custom_ml = Decimal(str(data['custom_ml']))
                if custom_ml < Decimal('0.1'):
                    return JsonResponse(
                        {'success': False, 'error': 'Minimum quantity is 0.1ml'}, 
                        status=400
                    )
                
                # Check stock for custom ml
                ml_per_package = 100  # Assuming standard package size is 100ml
                equivalent_packages = (custom_ml / Decimal(ml_per_package)).quantize(Decimal('0.01'))
                
                if equivalent_packages > cart_item.product.stock_quantity:
                    return JsonResponse({
                        'success': False,
                        'error': f'Not enough stock. Only {cart_item.product.stock_quantity} packages available.'
                    }, status=400)
                
                cart_item.custom_ml = custom_ml
                cart_item.save()
            
            else:
                return JsonResponse(
                    {'success': False, 'error': 'Invalid update data'}, 
                    status=400
                )
        
        # Recalculate cart totals
        cart = cart_item.cart
        cart_items = cart.items.select_related('product').annotate(
            item_total=ExpressionWrapper(
                Coalesce(F('custom_ml'), 0) * F('product__ml_price') + 
                Coalesce(F('quantity'), 0) * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
        cart_total = sum(item.item_total for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'cart_total': cart.item_count,
            'subtotal': float(cart_item.item_total if hasattr(cart_item, 'item_total') else cart_item.total_price),
            'cart_total_price': float(cart_total)
        })
        
    except (CartItem.DoesNotExist, json.JSONDecodeError, KeyError, ValueError) as e:
        return JsonResponse(
            {'success': False, 'error': str(e) or 'Invalid request'}, 
            status=400
        )

@require_POST
def remove_cart_item(request, item_id):
    """Remove an item from the cart"""
    try:
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
        
        cart_item = CartItem.objects.select_related('cart', 'product').get(
            id=item_id, 
            cart__session_key=request.session.session_key
        )
        
        product_name = cart_item.product.name
        cart = cart_item.cart
        cart_item.delete()
        
        # Recalculate cart totals
        cart_items = cart.items.select_related('product').annotate(
            item_total=ExpressionWrapper(
                Coalesce(F('custom_ml'), 0) * F('product__ml_price') + 
                Coalesce(F('quantity'), 0) * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
        cart_total = sum(item.item_total for item in cart_items)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': cart.item_count,
                'cart_total_price': float(cart_total),
                'message': f"Removed {product_name} from your cart."
            })
        
        messages.success(request, f"Removed {product_name} from your cart.")
        return redirect('catalog:view_cart')
        
    except CartItem.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {'success': False, 'error': 'Item not found in your cart'}, 
                status=404
            )
        messages.error(request, 'Item not found in your cart.')
        return redirect('catalog:view_cart')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {'success': False, 'error': f'Error removing item: {str(e)}'}, 
                status=500
            )
        messages.error(request, 'There was an error removing the item from your cart.')
        return redirect('catalog:view_cart')

def get_or_create_cart(request):
    """Helper function to get or create cart for current session"""
    if not request.session.session_key:
        request.session.create()
    
    cart, created = Cart.objects.get_or_create(
        session_key=request.session.session_key
    )
    return cart
