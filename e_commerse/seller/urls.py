from django.urls import path
from .views import add_product, seller_dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add-product/', add_product, name='add_product'),
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)