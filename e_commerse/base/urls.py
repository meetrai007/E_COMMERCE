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
    path('send-email-otp/', views.send_email_otp, name='send_email_otp'),
    path('validate-email-otp/', views.validate_email_otp, name='validate_email_otp'),
    path('user_account/',views.user_account, name='user_account'),
    path('test_email/',views.test_email, name='test_email'),
    # Other URL patterns
    path('logout/', LogoutView.as_view(), name='logout'),
    # Optional: Redirecting to the homepage after logout
    path('', RedirectView.as_view(url='/', permanent=False), name='homepage'), 

]


