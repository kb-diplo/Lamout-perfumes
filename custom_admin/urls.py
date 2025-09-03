from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='custom_admin/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='custom_admin:login'), name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/toggle-status/', views.update_product_status, name='product_toggle_status'),
    
    # Additional Admin Views
    path('categories/', views.manage_categories, name='manage_categories'),
    path('settings/', views.settings_view, name='settings'),
    path('gallery/', views.gallery_manager, name='gallery_manager'),
    path('gallery/upload/', views.gallery_upload, name='gallery_upload'),
    path('gallery/delete/', views.gallery_delete, name='gallery_delete'),
]
