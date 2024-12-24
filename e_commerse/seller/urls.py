from django.urls import path
from .views import add_product, seller_dashboard
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add-product/', add_product, name='add_product'),
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),
    # URL for seller registration
    path('register/', views.seller_register, name='seller_register'),

    # URL for seller login
    path('login/', views.seller_login, name='seller_login'),

    # URL for seller logout
    path('logout/', views.seller_logout, name='seller_logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)