# urls.py

# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView
from base import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('user_account/',views.account_page, name='user_account'),
    # Other URL patterns
    path('logout/', LogoutView.as_view(), name='logout'),
    # Optional: Redirecting to the homepage after logout
    path('', RedirectView.as_view(url='/', permanent=False), name='homepage'), 
    path('become-seller/', views.become_seller, name='become_seller'),

]


