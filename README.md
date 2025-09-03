# Lamout Perfume

A modern Django-based e-commerce website for premium perfumes with WhatsApp ordering integration and custom admin panel.

## Overview

Lamout Perfume is a specialized perfume retailer located in Neema HSE, Githunguri, offering authentic fragrances for men and women with convenient WhatsApp ordering, competitive pricing, and comprehensive product management.

## Features

### Customer Features
- **Perfume Catalog Showcase** - Visual display of 52+ premium perfume collections
- **Advanced Categorization** - Products organized by:
  - **Gender Collections**: Men's Collection (6 products), Ladies' Collection (15 products)
  - **Fragrance Types**: Woody (5), Fresh (7), Oriental (7), Floral (12), Unisex
- **Shopping Cart System** - Add products, adjust quantities, remove items
- **Flexible Ordering** - Full packages or custom milliliter portions
- **WhatsApp Integration** - Direct ordering via WhatsApp (+254616301107)
- **Responsive Design** - Mobile-first approach with Bootstrap 5
- **Modern UI** - Enhanced with animations, hover effects, and professional styling

### Admin Features
- **Custom Admin Panel** - Secure superuser-only access at `/custom-admin/`
- **Product Management** - Create, edit, delete products with image uploads
- **Category Management** - View product distribution across categories
- **Inventory Control** - Stock quantity and pricing management
- **Clean Authentication** - Django admin-style login without signup options

## Technology Stack

### Backend
- **Django 4.2.7** - Python web framework
- **SQLite** - Development database
- **Python 3.13** - Programming language

### Frontend
- **Bootstrap 5** - CSS framework for responsive design
- **HTML5/CSS3** - Structure and styling
- **JavaScript** - Interactive features

### Dependencies
- **django-crispy-forms 2.1** - Enhanced form rendering
- **crispy-bootstrap5 0.7** - Bootstrap 5 integration for forms
- **django-allauth** - User authentication (for admin only)
- **Pillow** - Image processing for product uploads

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "lamout perfumes web"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the website**
   - **Main Site**: `http://127.0.0.1:8000/`
   - **Custom Admin**: `http://127.0.0.1:8000/custom-admin/`
   - **Django Admin**: `http://127.0.0.1:8000/admin/`

## Project Structure

```
lamout perfumes web/
├── lamoutperfumes/          # Main project settings
├── home/                    # Home page app
├── catalog/                 # Perfume catalog and cart app
├── custom_admin/            # Custom admin panel app
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── catalog/            # Catalog templates
│   ├── custom_admin/       # Admin templates
│   ├── home/               # Home templates
│   ├── includes/           # Reusable components
│   └── errors/             # Error pages
├── static/                  # CSS, images, favicon
├── media/                   # Perfume product images (142 images)
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## Available Pages

### Customer Pages
- `/` - Home page with hero section and featured products
- `/catalog/` - Main perfume showcase with filtering by category
- `/catalog/mens/` - Men's perfumes collection page
- `/catalog/ladies/` - Ladies' perfumes collection page
- `/catalog/cart/` - Shopping cart with quantity management
- `/catalog/checkout/` - Checkout and WhatsApp order integration

### Admin Pages
- `/custom-admin/` - Custom admin dashboard (superuser only)
- `/custom-admin/products/` - Product management
- `/custom-admin/categories/` - Category overview and statistics
- `/admin/` - Django admin panel

## Pricing Structure

- **Per Milliliter**: KSH 100/ml for all perfumes
- **Package Pricing**: KSH 500 - KSH 2,500 depending on volume
- **Example**: Chanel No 5 - KSH 2,500 (50ml) or KSH 100/ml

## WhatsApp Integration

The custom order form generates formatted WhatsApp messages containing:
- Customer information (name, phone, location)
- Perfume specifications (name, category, scent type)
- Package preferences (ML quantity, bottle count, package size)
- Budget and delivery requirements
- Special requests

## Contact Information

- **Phone**: 0716301107 (WhatsApp)
- **Location**: Neema HSE, Githunguri
- **Business**: Lamout Perfume
- **CEO**: Munyua

## Development

### Key Apps

1. **Home App** - Landing page and basic navigation
2. **Catalog App** - Perfume listings, showcase, and order system

### Custom Features

- **Simplified Architecture** - Removed unnecessary apps (bag, checkout, products, profiles)
- **Clean URL Structure** - Only essential URLs for home, catalog, and admin
- **Dynamic Form Handling** - ML vs Package options in order form
- **WhatsApp Integration** - URL generation with encoded messages
- **Responsive Design** - Product grid with hover effects
- **Mobile-Optimized** - Navigation and user interface
- **No Authentication** - Streamlined user experience without login requirements

### URL Patterns

```python
# Main URLs
path("", include("home.urls")),
path("catalog/", include("catalog.urls")),
path("admin/", admin.site.urls),

# Catalog URLs
path('', views.showcase, name='showcase'),
path('mens/', views.mens_perfumes, name='mens_perfumes'),
path('ladies/', views.ladies_perfumes, name='ladies_perfumes'),
path('order/', views.contact_form, name='contact_form'),
path('order/success/', views.order_success, name='order_success'),
```

## License

© 2023-2025 Lamout Perfume. All rights reserved.

## Developer

**Portfolio**: [mbugualawrence.pythonanywhere.com](https://mbugualawrence.pythonanywhere.com)
