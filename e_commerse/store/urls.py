# urls.py

# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home_view,product_detail_view,search_products

urlpatterns = [
    path('', home_view, name='home'),
    path('product/<slug:slug>/', product_detail_view, name='product_detail'),
      path('search/', search_products, name='search_products'),

]

# Add this to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)