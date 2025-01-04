from django.contrib import admin
from .models import OTP

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('phone_number',)
