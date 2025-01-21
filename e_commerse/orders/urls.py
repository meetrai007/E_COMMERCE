from django.urls import path
from . import views

urlpatterns = [
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
