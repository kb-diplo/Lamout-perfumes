"""eau_royal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("", include("home.urls")),
    path("catalog/", include(("catalog.urls", "catalog"), namespace="catalog")),
    path("custom-admin/", include("custom_admin.urls", namespace="custom_admin")),
    path("admin/", admin.site.urls),  # Keep Django admin as fallback
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "home.views.error_404"
handler500 = "home.views.error_500"
