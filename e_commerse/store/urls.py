# urls.py
from django.urls import path
from .views import home_view, product_detail_view

urlpatterns = [
    path('', home_view, name='home'),
    path('product/<slug:slug>/', product_detail_view, name='product_detail'),
]
