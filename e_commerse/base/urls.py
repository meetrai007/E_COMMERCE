# urls.py

# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView
from base import views



urlpatterns = [
    path('user_account/',views.account_page, name='user_account'),
    # Other URL patterns
    path('logout/', LogoutView.as_view(), name='logout'),
    # Optional: Redirecting to the homepage after logout
    path('', RedirectView.as_view(url='/', permanent=False), name='homepage'), 
    path('become-seller/', views.become_seller, name='become_seller'),
    path('login-or-signup/', views.login_or_signup_with_otp, name='login_or_signup_with_otp'),

    path('profile/update/', views.update_profile, name='profile_update'),

]

# Custom error handler
handler404 = 'base.views.handler404'
# handler404 = 'base.views.handler500'
