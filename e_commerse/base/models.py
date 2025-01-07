from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta






class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    resend_count = models.IntegerField(default=0)
    last_resend_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return (now() - self.created_at).seconds <= 300  # Valid for 5 minutes

    def can_resend(self):
        if self.resend_count >= 3 and now().date() == self.last_resend_at.date():
            return False  # Exceeded daily limit
        if self.last_resend_at and (now() - self.last_resend_at).seconds < 60:
            return False  # Resend not allowed within 1 minute
        return True

    def reset_resend_count(self):
        if self.last_resend_at and self.last_resend_at.date() != now().date():
            self.resend_count = 0  # Reset count daily
