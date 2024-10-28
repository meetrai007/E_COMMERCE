# urls.py

# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from base import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('user_account/',views.user_account, name='user_account'),

]

