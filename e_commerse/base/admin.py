from django.contrib import admin
from .models import Userprofile
from .models import OTP

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('phone_number',)


@admin.register(Userprofile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone_number', 'first_name', 'last_name')
