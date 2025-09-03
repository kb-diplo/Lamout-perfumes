from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json

from catalog.models import Product
import os
from django.conf import settings

# Custom decorator to require superuser access
def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

# Custom decorator to check if user is staff
def staff_required(view_func):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/custom-admin/login/'
    )(view_func)
    return decorated_view

@superuser_required
def dashboard(request):
    # Get counts for dashboard
    product_count = Product.objects.count()
    
    context = {
        'product_count': product_count,
        'order_count': 0,  # Placeholder for future implementation
        'customer_count': 0,  # Placeholder for future implementation
        'total_revenue': 0,  # Placeholder for future implementation
        'recent_orders': [],  # Placeholder for future implementation
    }
    return render(request, 'custom_admin/dashboard.html', context)

# Product Views
@method_decorator(superuser_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'custom_admin/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset.order_by('name')

@method_decorator(superuser_required, name='dispatch')
class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'custom_admin/product_form.html'
    fields = ['name', 'description', 'category', 'price', 'ml_price', 'stock_quantity', 'is_featured']
    success_url = reverse_lazy('custom_admin:product_list')
    success_message = 'Product was created successfully!'
    
    def form_valid(self, form):
        # Set ml_price to 0 if not provided
        if not form.cleaned_data.get('ml_price'):
            form.instance.ml_price = 0
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

@method_decorator(superuser_required, name='dispatch')
class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'custom_admin/product_form.html'
    fields = ['name', 'description', 'category', 'price', 'ml_price', 'stock_quantity', 'is_featured']
    success_url = reverse_lazy('custom_admin:product_list')
    success_message = 'Product was updated successfully!'
    
    def form_valid(self, form):
        # Set ml_price to 0 if not provided
        if not form.cleaned_data.get('ml_price'):
            form.instance.ml_price = 0
            
        # Handle image clearing (kept for backward compatibility)
        if 'image-clear' in self.request.POST and self.request.POST['image-clear'] == 'on':
            if hasattr(self.object, 'image') and self.object.image:
                self.object.image.delete(save=False)
        
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

@superuser_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_name = product.name
    product.delete()
    messages.success(request, f'Product "{product_name}" was deleted successfully!')
    return redirect('custom_admin:product_list')

# AJAX View for Updating Product Status
@superuser_required
@require_POST
def update_product_status(request, pk):
    if request.is_ajax():
        product = get_object_or_404(Product, pk=pk)
        product.is_active = not product.is_active
        product.save()
        return JsonResponse({'status': 'success', 'is_active': product.is_active})
    return JsonResponse({'status': 'error'}, status=400)

@superuser_required
def manage_categories(request):
    """View to manage product categories"""
    # Get counts for different category types
    category_counts = {}
    
    # Product categories
    for category_code, category_name in Product.CATEGORY_CHOICES:
        count = Product.objects.filter(category=category_code).count()
        category_counts[category_code] = {
            'name': category_name,
            'count': count
        }
    
    context = {
        'categories': category_counts,
        'total_products': Product.objects.count(),
    }
    return render(request, 'custom_admin/manage_categories.html', context)

@superuser_required
def settings_view(request):
    """Admin settings view"""
    context = {
        'site_name': 'Lamout Perfumes',
        'total_products': Product.objects.count(),
        'featured_products': Product.objects.filter(is_featured=True).count(),
    }
    return render(request, 'custom_admin/settings.html', context)

@superuser_required
def gallery_manager(request):
    """Gallery management view"""
    # Get all image files from media directory
    media_path = settings.MEDIA_ROOT
    image_files = []
    
    if os.path.exists(media_path):
        for filename in os.listdir(media_path):
            if filename.lower().endswith(('.jpeg', '.jpg', '.png')) and filename.startswith('ER'):
                file_path = os.path.join(media_path, filename)
                file_size = os.path.getsize(file_path)
                image_files.append({
                    'filename': filename,
                    'size': file_size,
                    'url': f'/media/{filename}'
                })
    
    # Sort by filename
    image_files.sort(key=lambda x: x['filename'])
    
    context = {
        'image_files': image_files,
        'total_images': len(image_files)
    }
    return render(request, 'custom_admin/gallery_manager.html', context)

@superuser_required
@require_POST
def gallery_upload(request):
    """Handle image upload for gallery"""
    try:
        uploaded_files = request.FILES.getlist('images')
        if not uploaded_files:
            return JsonResponse({'success': False, 'error': 'No files uploaded'})
        
        uploaded_count = 0
        for uploaded_file in uploaded_files:
            # Validate file type
            if not uploaded_file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            # Generate filename with ER prefix
            import time
            timestamp = str(int(time.time()))
            file_extension = uploaded_file.name.split('.')[-1].lower()
            filename = f"ER{timestamp}_{uploaded_count}.{file_extension}"
            
            # Save file to media directory
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            uploaded_count += 1
        
        return JsonResponse({
            'success': True, 
            'message': f'{uploaded_count} images uploaded successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@superuser_required
@require_POST
def gallery_delete(request):
    """Handle image deletion from gallery"""
    try:
        data = json.loads(request.body)
        filename = data.get('filename')
        
        if not filename:
            return JsonResponse({'success': False, 'error': 'No filename provided'})
        
        # Security check - only allow deletion of ER prefixed files
        if not filename.startswith('ER'):
            return JsonResponse({'success': False, 'error': 'Invalid filename'})
        
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return JsonResponse({'success': True, 'message': 'Image deleted successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'File not found'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
