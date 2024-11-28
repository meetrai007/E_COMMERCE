from django.urls import path
from .views import add_product, seller_dashboard

urlpatterns = [
    path('add-product/', add_product, name='add_product'),
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),
]
